#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#
import json
import os
import sys

from time import sleep

from mlt.utils import process_helpers


def call_logs(config, args):
    """
    This method will check for `.push.josn`
    and provides run-id to _get_logs method to
    fetch logs.
    """
    if os.path.exists('.push.json'):
        with open('.push.json', 'r') as f:
            data = json.load(f)
    else:
        print("This app has not been deployed yet, "
              "there are no logs to display.")
        sys.exit(1)

    app_run_id = data['app_run_id'].split("-")

    if len(app_run_id) < 2:
        print("Please re-deploy app again, something went wrong.")
        sys.exit(1)

    prefix = "-".join([config["name"], app_run_id[0], app_run_id[1]])
    namespace = config['namespace']
    retires = args["--retries"]

    # check for pod readiness before fetching logs.
    _check_for_pods_readiness(namespace, prefix, retires)

    since = args["--since"]
    _get_logs(prefix, since, namespace)


def _get_logs(prefix, since, namespace):
    """
    Fetches logs using kubetail
    """
    log_cmd = "kubetail {} --since {} " \
              "--namespace {}".format(prefix, since, namespace)
    try:
        # TODO: remove shell=True. and make log_cmd as List.
        logs = process_helpers.run_popen(log_cmd, shell=True)

        while True:
            output = logs.stdout.readline()
            if output == '' and logs.poll() is not None:
                error = logs.stderr.readline()
                if error:
                    raise Exception(error)
                break
            if output:
                print(output.strip())

    except Exception as ex:
        if 'command not found' in str(ex):
            print("Please install `{}`. "
                  "It is a prerequisite for `mlt logs` "
                  "to work".format(str(ex).split()[1]))
        else:
            print("Exception: {}".format(ex))
        sys.exit()

def _get_pod_names(namespace, filter_tag):
    pod_names = []
    pods = process_helpers.run_popen(
        "kubectl get pods --namespace {} ".format(namespace), shell=True
    ).stdout.read().decode('utf-8').strip().splitlines()
    if pods:
        for pod_name in pods:
            if filter_tag in pod_name:
                pod_names.append(str(pod_name.split(" ")[0]))
    else:
        raise ValueError(
            "No pods found in namespace: {}".format(namespace))
    return pod_names

def _check_for_pods_readiness(namespace, filter_tag, retries):
    pod_names = _get_pod_names(namespace, filter_tag)
    count = 0
    for pod_name in pod_names:
        if _is_ready(namespace, pod_name, retries):
            count = count + 1

    if not len(pod_names) == count:
        print("Tailing logs from pods which are UP")


def _is_ready(namespace, podname, retires):
    print("Checking for pod readiness: {}".format(podname))
    tries = 0
    while True:
        pod = process_helpers.run_popen(
            "kubectl get pods --namespace {} {} -o json".format(
                namespace, podname),
            shell=True).stdout.read().decode('utf-8')
        if not pod:
            continue

        # check if pod is in running state
        # gcr stores an auth token which could be returned as part
        # of the pod json data
        pod = json.loads(pod)
        if pod.get('items') or pod.get('status'):
            # if there's more than 1 thing returned, we have
            # `pod['items']['status']` otherwise we will always have
            # `pod['status'], so by the second if below we're safe
            # first item is what we care about (or only item)
            if pod.get('items'):
                pod = pod['items'][0]
            if pod['status']['phase'] == 'Running':
                print("{} is UP".format(podname))
                return True

        if tries == retires:
            print("Max retires reached.")
            return False
        tries += 1
        print("Retrying {}/{}".format(
            tries, retires))
        sleep(1)

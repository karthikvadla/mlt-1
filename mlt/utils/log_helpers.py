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
    since = args["--since"]
    namespace = config['namespace']
    _get_logs(prefix, since, namespace)


def _get_logs(prefix, since, namespace):
    """
    Fetches logs using kubetail
    """
    print("Tailing logs, Please wait for few seconds...")
    # TODO: change this to check looping through pods status
    sleep(10)
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

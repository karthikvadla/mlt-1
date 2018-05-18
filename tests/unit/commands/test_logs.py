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

from __future__ import print_function

import pytest

import uuid
from mlt.utils.log_helpers import check_for_pods_readiness, get_namespace_pods
from mlt.commands.logs import LogsCommand

from test_utils.io import catch_stdout


@pytest.fixture
def json_mock(patch):
    return patch('log_helpers.json')

@pytest.fixture
def open_mock(patch):
    return patch('open')

@pytest.fixture
def sleep_mock(patch):
    return patch('log_helpers.sleep')

@pytest.fixture
def process_helpers(patch):
    return patch('log_helpers.process_helpers.run_popen')

@pytest.fixture
def os_path_mock(patch):
    return patch('log_helpers.os.path')

@pytest.fixture
def check_for_pods_readiness_mock(patch):
    return patch('log_helpers.check_for_pods_readiness')

@pytest.fixture
def get_namespace_pods_mock(patch):
    return patch('log_helpers.get_namespace_pods')

@pytest.fixture
def verify_init(patch):
    return patch('config_helpers.load_config')

def test_logs_get_logs(json_mock, open_mock, verify_init, sleep_mock,
                       check_for_pods_readiness_mock,
                       process_helpers, os_path_mock):
    run_id = str(uuid.uuid4())
    os_path_mock.exists.return_value = True
    json_mock_data = {
        'last_remote_container': 'gcr.io/app_name:container_id',
        'last_push_duration': 0.18889,
        'app_run_id': run_id}
    json_mock.load.return_value = json_mock_data
    logs_command = LogsCommand({'logs': True, '--since': '1m', '--retries':5})
    logs_command.config = {'name': 'app', 'namespace': 'namespace'}

    log_value = '-'.join(['app', run_id])
    check_for_pods_readiness_mock.return_value = True
    process_helpers.return_value.stdout.readline.side_effect = [log_value, '']
    process_helpers.return_value.poll.return_value = 1
    process_helpers.return_value.stderr.readline.return_value = ''
    with catch_stdout() as caught_output:
        logs_command.action()
        output = caught_output.getvalue()
    assert log_value in output

def test_logs_no_push_json_file(open_mock, verify_init, sleep_mock,
                                process_helpers, os_path_mock):
    os_path_mock.exists.return_value = False
    logs_command = LogsCommand({'logs': True, '--since': '1m', '--retries':5})
    logs_command.config = {'name': 'app', 'namespace': 'namespace'}

    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit):
            logs_command.action()
        output = caught_output.getvalue()

    assert "This app has not been deployed yet" in output

def test_logs_corrupted_app_run_id(json_mock, open_mock, sleep_mock,
                                   verify_init, process_helpers, os_path_mock):
    run_id = '31dea6fc'
    os_path_mock.exists.return_value = True
    json_mock_data = {
        'last_remote_container': 'gcr.io/app_name:container_id',
        'last_push_duration': 0.18889,
        'app_run_id': run_id}
    json_mock.load.return_value = json_mock_data
    logs_command = LogsCommand({'logs': True, '--since': '1m', '--retries':5})
    logs_command.config = {'name': 'app', 'namespace': 'namespace'}

    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit):
            logs_command.action()
        output = caught_output.getvalue()

    assert"Please re-deploy app again, something went wrong." in output

def test_logs_exception(json_mock, open_mock, verify_init, sleep_mock,
                        check_for_pods_readiness_mock,
                        process_helpers, os_path_mock):
    run_id = str(uuid.uuid4())
    os_path_mock.exists.return_value = True
    json_mock_data = {
        'last_remote_container': 'gcr.io/app_name:container_id',
        'last_push_duration': 0.18889,
        'app_run_id': run_id}
    check_for_pods_readiness_mock.return_value = True
    json_mock.load.return_value = json_mock_data
    logs_command = LogsCommand({'logs': True, '--since': '1m', '--retries':5})
    logs_command.config = {'name': 'app', 'namespace': 'namespace'}

    process_helpers.side_effect = OSError

    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit):
            logs_command.action()
        output = caught_output.getvalue()

    assert "Exception:" in output


def test_logs_command_not_found(json_mock, open_mock, sleep_mock, check_for_pods_readiness_mock,
                                verify_init, process_helpers, os_path_mock):
    run_id = str(uuid.uuid4())
    os_path_mock.exists.return_value = True
    json_mock_data = {
        'last_remote_container': 'gcr.io/app_name:container_id',
        'last_push_duration': 0.18889,
        'app_run_id': run_id}
    json_mock.load.return_value = json_mock_data
    logs_command = LogsCommand({'logs': True, '--since': '1m', '--retries':5})
    logs_command.config = {'name': 'app', 'namespace': 'namespace'}
    check_for_pods_readiness_mock.return_value = True
    command_not_found = '/bin/sh: kubetail: command not found'
    process_helpers.return_value.stdout.readline.return_value = ''
    process_helpers.return_value.poll.return_value = 1
    process_helpers.return_value.\
        stderr.readline.side_effect = Exception(command_not_found)
    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit):
            logs_command.action()
        output = caught_output.getvalue()

    assert 'It is a prerequisite' in output

def test_logs_check_for_pods_readiness(get_namespace_pods_mock):
    run_id = str(uuid.uuid4()).split("-")
    filter_tag = "-".join(["app", run_id[0], run_id[1]])
    get_namespace_pods_mock.return_value = (True, 1,
                                            [filter_tag+"-ps-"+run_id[3]+" 1/1  Running  0  16d",
                                             filter_tag+"-worker1-"+run_id[3]+" 1/1  Running  0  16d",
                                             filter_tag+"-worker2-"+run_id[3]+" 1/1  Running  0  16d"])

    with catch_stdout() as caught_output:
        found = check_for_pods_readiness(namespace='namespace', filter_tag=filter_tag, retries=5)
        output = caught_output.getvalue()

    assert found == True
    assert "Checking for pod(s) readiness" in output

def test_logs_check_for_pods_readiness_no_logs_msg(get_namespace_pods_mock):
    run_id = str(uuid.uuid4()).split("-")
    filter_tag = "-".join(["app", run_id[0], run_id[1]])
    get_namespace_pods_mock.return_value = (False, 5, [])

    with catch_stdout() as caught_output:
        found = check_for_pods_readiness(namespace='namespace', filter_tag=filter_tag, retries=5)
        output = caught_output.getvalue()

    assert found == False
    assert "No logs to show because no pods founds for this job." in output

def test_logs_check_for_pods_readiness_max_retries_reached(get_namespace_pods_mock):
    run_id = str(uuid.uuid4()).split("-")
    filter_tag = "-".join(["app", run_id[0], run_id[1]])
    get_namespace_pods_mock.return_value = (True, 5, [filter_tag+"-ps-"+run_id[3]+" 1/1  Running  0  16d"])

    with catch_stdout() as caught_output:
        found = check_for_pods_readiness(namespace='namespace', filter_tag=filter_tag, retries=5)
        output = caught_output.getvalue()

    assert found == True
    assert "Max retries Reached." in output

def test_logs_get_namespace_pods(process_helpers):
    run_id = str(uuid.uuid4()).split("-")
    filter_tag = "-".join(["app", run_id[0], run_id[1]])

    all_pods = [ "random_pod_1",
                 "random_pod_2",
                 filter_tag + "-ps-" + run_id[3] + " 1/1  Running  0  16d",
                 filter_tag + "-worker1-" + run_id[3] + " 1/1  Running  0  16d",
                 filter_tag + "-worker2-" + run_id[3] + " 1/1  Running  0  16d"]

    all_pods_str = "\n".join([ "random_pod_1",
                               "random_pod_2",
                               filter_tag + "-ps-" + run_id[3] + " 1/1  Running  0  16d",
                               filter_tag + "-worker1-" + run_id[3] + " 1/1  Running  0  16d",
                               filter_tag + "-worker2-" + run_id[3] + " 1/1  Running  0  16d"])

    process_helpers.return_value.stdout.read.return_value = all_pods_str

    _, _, pods = get_namespace_pods(namespace='namespace', filter_tag=filter_tag, retries=5)

    assert len(pods) == len(all_pods)

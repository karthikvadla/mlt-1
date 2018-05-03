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
from mlt.commands.events import EventsCommand
from test_utils.io import catch_stdout


@pytest.fixture
def json_mock(patch):
    return patch('json')


@pytest.fixture
def open_mock(patch):
    return patch('open')


@pytest.fixture
def process_helpers(patch):
    return patch('process_helpers.run_popen')

@pytest.fixture
def verify_init(patch):
    return patch('config_helpers.load_config')


def test_events_get_events(json_mock, open_mock, verify_init, process_helpers):
    run_id = str(uuid.uuid4())
    json_mock_data = {
        'last_remote_container': 'gcr.io/app_name:container_id',
        'last_push_duration': 0.18889,
        'app_run_id': run_id}
    json_mock.load.return_value = json_mock_data


    events_command = EventsCommand({'events': True})
    events_command.config = {'name': 'app', 'namespace': 'namespace'}

    event_value = '-'.join(['app', run_id])
    process_helpers.return_value.stdout.read.side_effect = [event_value, '']
    process_helpers.return_value.poll.return_value = 1
    with catch_stdout() as caught_output:
        events_command.action()
        output = caught_output.getvalue()
    assert event_value in output
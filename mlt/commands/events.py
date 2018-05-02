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

import sys
import json

from mlt.commands import Command
from mlt.utils import (process_helpers,
                       config_helpers)


class EventsCommand(Command):
    def __init__(self, args):
        super(EventsCommand, self).__init__(args)
        self.config = config_helpers.load_config()

    def action(self):
        """
        Display events for the latest run
        """
        with open('.push.json', 'r') as f:
            data = json.load(f)

        app_run_id = data['app_run_id'].split('-')
        filter_tag = "-".join([self.config["name"],
                               app_run_id[0],
                               app_run_id[1],
                               app_run_id[2],
                               app_run_id[3]])
        namespace = self.config['namespace']
        self.get_events(filter_tag, namespace)

    @staticmethod
    def get_events(filter_tag, namespace):

        awk = 'awk \'NR=1 || /{}/\''.format(filter_tag)
        events_cmd = "kubectl get events " \
                     "--namespace {} | {}"\
            .format(namespace, awk)

        events = process_helpers.run_popen(events_cmd, shell=True)

        while True:
            output = events.stdout.read(1)
            if output == '' and events.poll() is not None:
                break
            if output is not '':
                sys.stdout.write(output)
                sys.stdout.flush()

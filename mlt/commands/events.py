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
import os

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
        self.call_events()

    def call_events(self):
        """
        This method will check for `.push.josn`
        and provides run-id to _get_event method to
        fetch events.
        """
        if os.path.exists('.push.json'):
            with open('.push.json', 'r') as f:
                data = json.load(f)
        else:
            print("This app has not been deployed yet, "
                  "there are no logs to display.")
            sys.exit(1)

        app_run_id = data['app_run_id'].split("-")

        if len(app_run_id) < 4:
            print("Please re-deploy app again, something went wrong.")
            sys.exit(1)

        filter_tag = "-".join([self.config["name"],
                               app_run_id[0],
                               app_run_id[1]])
        namespace = self.config['namespace']
        self._get_events(filter_tag, namespace)

    @staticmethod
    def _get_events(filter_tag, namespace):
        """
         Fetches events
        """
        events_cmd = ["kubectl", "get", "events", "--namespace", namespace]
        try:
            events = process_helpers.run_popen(events_cmd)
            first_line = True
            header = events.stdout.readline()
            while True:
                output = events.stdout.readline()
                if output == '' and events.poll() is not None:
                    error = events.stderr.readline()
                    if error:
                        raise Exception(error)
                    break

                if output is not '' and filter_tag in output:
                    if first_line:
                        print(header)
                        first_line = False
                    sys.stdout.write(output)
                    sys.stdout.flush()

        except Exception as ex:
            print("Exception: {}".format(ex))
            sys.exit()

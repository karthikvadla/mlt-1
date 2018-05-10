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

from mlt.commands import Command
from mlt.utils import (process_helpers,
                       config_helpers)


class LogsCommand(Command):
    def __init__(self, args):
        super(LogsCommand, self).__init__(args)
        self.config = config_helpers.load_config()

    def action(self):
        """
        Display logs from all pods for latest run.

        """
        if os.path.exists('.push.json'):
            with open('.push.json', 'r') as f:
                data = json.load(f)
        else:
            print("This app has not been deployed yet,"
                  "there are no logs to display.")
            sys.exit(1)

        app_run_id = data['app_run_id'].split("-")

        if len(app_run_id) < 2:
            print("Please re-deploy app again, something went wrong.")
            sys.exit(1)

        prefix = "-".join([self.config["name"], app_run_id[0], app_run_id[1]])
        since = self.args["--since"]
        namespace = self.config['namespace']
        self.get_logs(prefix, since, namespace)

    @staticmethod
    def get_logs(prefix, since, namespace):

        log_cmd = ["kubetail", prefix, "--since",
                   since, "--namespace", namespace]
        try:
            logs = process_helpers.run_popen(log_cmd)

            while True:
                output = logs.stdout.readline()
                if output == '' and logs.poll() is not None:
                    break
                if output:
                    print(output.strip())

        except Exception as ex:
            print("Exception: {}".format(ex))
            sys.exit()

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
import time

from mlt.commands import Command
from mlt.utils import (config_helpers, log_helpers)


class LogsCommand(Command):
    def __init__(self, args):
        super(LogsCommand, self).__init__(args)
        self.config = config_helpers.load_config()

    def action(self):
        """
        Display logs from all pods for latest run.

        """
        print("Tailing logs, Please wait for few seconds...")
        time.sleep(10)
        log_helpers.call_logs(self.config, self.args)

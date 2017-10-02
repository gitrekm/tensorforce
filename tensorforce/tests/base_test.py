# Copyright 2017 reinforce.io. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from six.moves import xrange
import sys

from tensorforce.execution import Runner


class BaseTest(object):

    agent = None
    deterministic = None

    def base_test(self, name, environment, network_spec, config):
        self.__class__.agent(
            states_spec=environment.states,
            actions_spec=environment.actions,
            network_spec=network_spec,
            config=config
        )

        sys.stdout.write('\n{} ({}):'.format(self.__class__.agent.__name__, name))
        sys.stdout.flush()

        passed = 0
        for _ in xrange(5):

            agent = self.__class__.agent(
                states_spec=environment.states,
                actions_spec=environment.actions,
                network_spec=network_spec,
                config=config
            )
            runner = Runner(agent=agent, environment=environment)

            def episode_finished(r):
                return r.episode < 100 or not all(rw / ln >= 0.8 for rw, ln in zip(r.episode_rewards[-100:], r.episode_lengths[-100:]))

            runner.run(episodes=3000, deterministic=self.__class__.deterministic, episode_finished=episode_finished)

            sys.stdout.write(' ' + str(runner.episode))
            sys.stdout.flush()
            if runner.episode < 3000:
                passed += 1

        sys.stdout.write('\n==> passed: {}\n'.format(passed))
        sys.stdout.flush()
        self.assertTrue(passed >= 4)
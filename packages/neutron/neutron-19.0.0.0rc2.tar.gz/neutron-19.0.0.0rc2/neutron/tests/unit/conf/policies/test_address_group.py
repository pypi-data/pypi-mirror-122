# Copyright (c) 2021 Red Hat Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_policy import policy as base_policy

from neutron import policy
from neutron.tests.unit.conf.policies import base


class AddressGroupAPITestCase(base.PolicyBaseTestCase):

    def setUp(self):
        super(AddressGroupAPITestCase, self).setUp()
        self.target = {'project_id': self.project_id}

    def test_system_reader_can_get_address_group(self):
        self.assertTrue(
            policy.enforce(self.system_reader_ctx,
                           "get_address_group", self.target))

    def test_project_reader_can_get_address_group(self):
        self.assertTrue(
            policy.enforce(self.project_reader_ctx,
                           "get_address_group", self.target))

    def test_system_reader_can_get_any_address_group(self):
        target = {'project_id': 'some-other-project'}
        self.assertTrue(
            policy.enforce(self.system_reader_ctx,
                           "get_address_group", target))

    def test_project_reader_can_not_get_address_group_other_tenant(self):
        target = {'project_id': 'some-other-project'}
        self.assertRaises(
            base_policy.PolicyNotAuthorized,
            policy.enforce,
            self.project_reader_ctx, "get_address_group", target)

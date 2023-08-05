# Copyright 2019 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import datetime
from unittest import mock

from neutron_lib import context
from oslo_utils import timeutils

from neutron.common.ovn import constants
from neutron.common.ovn import exceptions
from neutron.common.ovn import hash_ring_manager
from neutron.db import ovn_hash_ring_db as db_hash_ring
from neutron import service
from neutron.tests.unit import testlib_api

HASH_RING_TEST_GROUP = 'test_group'


class TestHashRingManager(testlib_api.SqlTestCaseLight):

    def setUp(self):
        super(TestHashRingManager, self).setUp()
        self.hash_ring_manager = hash_ring_manager.HashRingManager(
            HASH_RING_TEST_GROUP)
        self.admin_ctx = context.get_admin_context()

    def _verify_hashes(self, hash_dict):
        for uuid_, target_node in hash_dict.items():
            self.assertEqual(target_node,
                             self.hash_ring_manager.get_node(uuid_))

    def test_get_node(self):
        # Use pre-defined UUIDs to make the hashes predictable
        node_1_uuid = db_hash_ring.add_node(
            self.admin_ctx, HASH_RING_TEST_GROUP, 'node-1')
        node_2_uuid = db_hash_ring.add_node(
            self.admin_ctx, HASH_RING_TEST_GROUP, 'node-2')

        hash_dict_before = {'fake-uuid': node_1_uuid,
                            'fake-uuid-0': node_2_uuid}
        self._verify_hashes(hash_dict_before)

    def test_get_node_no_active_nodes(self):
        self.assertRaises(
            exceptions.HashRingIsEmpty, self.hash_ring_manager.get_node,
            'fake-uuid')

    def test_ring_rebalance(self):
        # Use pre-defined UUIDs to make the hashes predictable
        node_1_uuid = db_hash_ring.add_node(
            self.admin_ctx, HASH_RING_TEST_GROUP, 'node-1')
        node_2_uuid = db_hash_ring.add_node(
            self.admin_ctx, HASH_RING_TEST_GROUP, 'node-2')

        # Add another node from a different host
        with mock.patch.object(db_hash_ring, 'CONF') as mock_conf:
            mock_conf.host = 'another-host-52359446-c366'
            another_host_node = db_hash_ring.add_node(
                self.admin_ctx, HASH_RING_TEST_GROUP, 'another-host')

        # Assert all nodes are alive in the ring
        self.hash_ring_manager.refresh()
        self.assertEqual(3, len(self.hash_ring_manager._hash_ring.nodes))

        # Hash certain values against the nodes
        hash_dict_before = {'fake-uuid': node_1_uuid,
                            'fake-uuid-0': node_2_uuid,
                            'fake-uuid-ABCDE': another_host_node}
        self._verify_hashes(hash_dict_before)

        # Mock utcnow() as the HASH_RING_NODES_TIMEOUT have expired
        # already and touch the nodes from our host
        fake_utcnow = timeutils.utcnow() - datetime.timedelta(
            seconds=constants.HASH_RING_NODES_TIMEOUT)
        with mock.patch.object(timeutils, 'utcnow') as mock_utcnow:
            mock_utcnow.return_value = fake_utcnow
            db_hash_ring.touch_nodes_from_host(
                self.admin_ctx, HASH_RING_TEST_GROUP)

        # Now assert that the ring was re-balanced and only the node from
        # another host is marked as alive
        self.hash_ring_manager.refresh()
        self.assertEqual([another_host_node],
                         list(self.hash_ring_manager._hash_ring.nodes.keys()))

        # Now only "another_host_node" is alive, all values should hash to it
        hash_dict_after_rebalance = {'fake-uuid': another_host_node,
                                     'fake-uuid-0': another_host_node,
                                     'fake-uuid-ABCDE': another_host_node}
        self._verify_hashes(hash_dict_after_rebalance)

        # Now touch the nodes so they appear active again
        db_hash_ring.touch_nodes_from_host(
            self.admin_ctx, HASH_RING_TEST_GROUP)
        self.hash_ring_manager.refresh()

        # The ring should re-balance and as it was before
        self._verify_hashes(hash_dict_before)

    @mock.patch.object(service, '_get_api_workers', return_value=2)
    def test__wait_startup_before_caching(self, api_workers):
        db_hash_ring.add_node(self.admin_ctx, HASH_RING_TEST_GROUP, 'node-1')

        # Assert it will return True until until we equal api_workers
        self.assertTrue(self.hash_ring_manager._wait_startup_before_caching)
        self.assertTrue(self.hash_ring_manager._check_hashring_startup)

        db_hash_ring.add_node(self.admin_ctx, HASH_RING_TEST_GROUP, 'node-2')

        # Assert it's now False. Waiting is not needed anymore
        self.assertFalse(self.hash_ring_manager._wait_startup_before_caching)
        self.assertFalse(self.hash_ring_manager._check_hashring_startup)

        # Now assert that since the _check_hashring_startup has been
        # flipped, we no longer will read from the database
        with mock.patch.object(hash_ring_manager.db_hash_ring,
                               'get_active_nodes') as get_nodes_mock:
            self.assertFalse(
                self.hash_ring_manager._wait_startup_before_caching)
            self.assertFalse(get_nodes_mock.called)

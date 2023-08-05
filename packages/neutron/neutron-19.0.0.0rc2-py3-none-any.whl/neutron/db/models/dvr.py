# Copyright 2016 Hewlett-Packard Development Company, L.P.
# All rights reserved.
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

from neutron_lib.db import model_base
import sqlalchemy as sa


class DistributedVirtualRouterMacAddress(model_base.BASEV2):
    """Represents a v2 neutron distributed virtual router mac address."""

    __tablename__ = 'dvr_host_macs'

    host = sa.Column(sa.String(255), primary_key=True, nullable=False)
    mac_address = sa.Column(sa.String(32), nullable=False, unique=True)


class DvrFipGatewayPortAgentBinding(model_base.BASEV2):
    """Represents a binding of agent's FIP gateway port and L3 agent.

    Each L3 DVR agent can only have one FIP gateway port per network.
    This table represents this constraint.
    """

    __tablename__ = 'dvr_fip_gateway_port_network'

    network_id = sa.Column(sa.String(36), sa.ForeignKey("networks.id",
                                                        ondelete="CASCADE"),
                           primary_key=True)
    agent_id = sa.Column(sa.String(36), sa.ForeignKey("agents.id",
                                                      ondelete="CASCADE"),
                         primary_key=True)

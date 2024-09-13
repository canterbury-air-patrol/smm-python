# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Missions
"""

from smm_client.assets import SMMAsset
from smm_client.organizations import SMMOrganization
from smm_client.types import SMMPoint


class SMMMission:
    """
    Search Management Map - Mission
    """

    def __init__(self, connection, mission_id: int, name: str):
        self.connection = connection
        self.id = mission_id
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.id})"

    def url_component(self, page: str):
        return f"/mission/{self.id}/{page}"

    def add_member(self, user: str):
        self.connection.post(self.url_component("users/add/"), data={"user": user})

    def add_organization(self, org: SMMOrganization):
        self.connection.post(self.url_component("organizations/add/"), data={"organization": org.id})

    def add_asset(self, asset: SMMAsset):
        self.connection.post(self.url_component("assets/"), data={"asset": asset.id})

    def remove_asset(self, asset: SMMAsset):
        self.connection.get(self.url_component(f"assets/{asset.id}/remove/"))

    def close(self):
        self.connection.get(self.url_component("close/"))

    def add_waypoint(self, point: SMMPoint, label: str):
        self.connection.post(
            self.url_component("/data/pois/create/"), {"lat": point.lat, "lon": point.lon, "label": label}
        )

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

    def __url_component(self, page: str):
        return f"/mission/{self.id}/{page}"

    def add_member(self, user: str):
        """
        Add a member to this mission
        """
        self.connection.post(self.__url_component("users/add/"), data={"user": user})

    def add_organization(self, org: SMMOrganization):
        """
        Add an organization to this mission
        """
        self.connection.post(self.__url_component("organizations/add/"), data={"organization": org.id})

    def add_asset(self, asset: SMMAsset):
        """
        Add an asset to this mission
        """
        self.connection.post(self.__url_component("assets/"), data={"asset": asset.id})

    def remove_asset(self, asset: SMMAsset):
        """
        Remove an asset from this mission
        """
        self.connection.get(self.__url_component(f"assets/{asset.id}/remove/"))

    def close(self):
        """
        Close this mission
        """
        self.connection.get(self.__url_component("close/"))

    def add_waypoint(self, point: SMMPoint, label: str):
        """
        Add a way point to this mission
        """
        self.connection.post(
            self.__url_component("/data/pois/create/"), {"lat": point.lat, "lon": point.lon, "label": label}
        )

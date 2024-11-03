# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Missions
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from smm_client.geometry import SMMLine, SMMPoi

if TYPE_CHECKING:
    from smm_client.assets import SMMAsset
    from smm_client.organizations import SMMOrganization
    from smm_client.types import SMMPoint


class SMMMission:
    """
    Search Management Map - Mission
    """

    def __init__(self, connection, mission_id: int, name: str) -> None:
        self.connection = connection
        self.id = mission_id
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    def __url_component(self, page: str) -> str:
        return f"/mission/{self.id}/{page}"

    def add_member(self, user: str) -> None:
        """
        Add a member to this mission
        """
        self.connection.post(self.__url_component("users/add/"), data={"user": user})

    def add_organization(self, org: SMMOrganization) -> None:
        """
        Add an organization to this mission
        """
        self.connection.post(self.__url_component("organizations/add/"), data={"organization": org.id})

    def add_asset(self, asset: SMMAsset) -> None:
        """
        Add an asset to this mission
        """
        self.connection.post(self.__url_component("assets/"), data={"asset": asset.id})

    def remove_asset(self, asset: SMMAsset) -> None:
        """
        Remove an asset from this mission
        """
        self.connection.get(self.__url_component(f"assets/{asset.id}/remove/"))

    def set_asset_command(self, asset: SMMAsset, command: str, reason: str, point: SMMPoint | None = None) -> None:
        """
        Set the command for a specific asset
        """
        data = {
            "asset": asset.id,
            "command": command,
            "reason": reason,
        }
        if point is not None:
            data["latitude"] = point.latitude
            data["longitude"] = point.longitude
        self.connection.post(self.__url_component("assets/command/set/"), data)

    def close(self) -> None:
        """
        Close this mission
        """
        self.connection.get(self.__url_component("close/"))

    def assets(self, include: str = "active") -> list[str]:
        """
        Get all the assets in this mission

        Use include="removed" to see get all assets that were ever in the mission
        """
        return self.connection.get_json(self.__url_component(f"assets/?include_removed={include == "removed"}"))

    def add_waypoint(self, point: SMMPoint, label: str) -> SMMPoi | None:
        """
        Add a way point to this mission
        """
        results = self.connection.post(
            self.__url_component("data/pois/create/"), {"lat": point.lat, "lon": point.lng, "label": label}
        )
        if results.status_code == requests.codes["ok"]:
            json_obj = results.json()
            return SMMPoi(self, json_obj["features"][0]["properties"]["pk"])
        return None

    def add_line(self, points: list[SMMPoint], label: str) -> SMMLine | None:
        """
        Add a line to this mission
        """
        data = {
            "points": len(points),
            "label": label,
        }
        i = 0
        for point in points:
            data[f"point{i}_lat"] = point.lat
            data[f"point{i}_lng"] = point.lng
            i = i + 1
        results = self.connection.post(self.__url_component("data/pois/create/"), data)
        if results.status_code == requests.codes["ok"]:
            json_obj = results.json()
            return SMMPoi(self, json_obj["features"][0]["properties"]["pk"])
        return None

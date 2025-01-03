# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Assets
"""

from __future__ import annotations

from json import JSONDecodeError

from smm_client.search import SMMSearch
from smm_client.types import SMMPoint


class SMMAssetStatusValue:
    # pylint: disable=R0903
    """
    Search Management Map - Asset Status Value
    """

    def __init__(self, value_id: int, name: str, description: str, *, inop: bool) -> None:
        self.id = value_id
        self.name = name
        self.inop = inop
        self.description = description


class SMMAssetStatus:
    # pylint: disable=R0903
    """
    Search Management Map - Asset Status
    """

    def __init__(self, asset: SMMAsset, data: dict) -> None:
        self.asset = asset
        self.status = data["status"]
        self.inop = data["inop"]
        self.since = data["since"]
        self.notes = data["notes"]


class SMMAssetCommand:
    # pylint: disable=R0903, R0902
    """
    Search Management Map - Asset Command
    """

    def __init__(self, asset: SMMAsset, data: dict) -> None:
        self.asset = asset
        self.issued = data["issued"]
        self.issued_by = data["issued_by"]
        self.command = data["action_txt"]
        if "latitude" in data and "longitude" in data:
            self.position = SMMPoint(data["latitude"], data["longitude"])
        self.reason = data["reason"]
        self.responded_by = data["response"]["by"]
        self.response_type = data["response"]["type"]
        self.response_message = data["response"]["message"]


class SMMAsset:
    # pylint: disable=R0903
    """
    Search Management Map - Asset
    """

    def __init__(self, connection, asset_id: int, name: str) -> None:
        self.connection = connection
        self.id = asset_id
        self.name = name

    def __url_component(self, page: str) -> str:
        return f"/assets/{self.id}/{page}"

    def get_status(self) -> SMMAssetStatus | None:
        """
        Get the current status of this asset
        """
        data = self.connection.get_json(self.__url_component("status/"))
        if data is not None:
            return SMMAssetStatus(self, data)
        return None

    def set_status(self, status: str, notes: str) -> None:
        """
        Update the status of this asset
        """
        self.connection.post(
            self.__url_component("status/"),
            data={
                "value_id": status,
                "notes": notes,
            },
        )

    def get_command(self) -> SMMAssetCommand | None:
        """
        Get the command that currently applies to this asset
        """
        data = self.connection.get_json(self.__url_component("command/"))
        if data is not None:
            return SMMAssetCommand(self, data)
        return None

    def set_position(
        self, lat: float, lon: float, fix: int, alt: int | None, heading: int | None
    ) -> SMMAssetCommand | None:
        # pylint: disable=R0913,R0917
        """
        Set/Update the position of this asset
        Will return the current asset command, if any
        """
        data = self.connection.post(
            f"/data/assets/{self.id}/position/add/",
            data={"lat": lat, "lon": lon, "fix": fix, "alt": alt, "heading": heading},
        )
        try:
            return SMMAssetCommand(self, data.json())
        except JSONDecodeError:
            return None

    def get_next_search(self, lat: float, lon: float) -> SMMSearch | None:
        """
        Get the nearest search for this asset
        Note: queued searches will be run in order before unqueued searches are looked for by distance
        """
        data = self.connection.post(
            "/search/find/closest/", data={"asset_id": self.id, "latitude": lat, "longitude": lon}
        )
        try:
            return SMMSearch(self.connection, list(filter(len, data.json()["object_url"].split("/")))[-1])
        except JSONDecodeError:
            return None

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"


class SMMAssetType:
    # pylint: disable=R0903
    """
    Search Management Map - Asset Type
    """

    def __init__(self, connection, type_id: int, name: str) -> None:
        self.connection = connection
        self.id = type_id
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

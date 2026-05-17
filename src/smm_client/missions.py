# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Missions
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from smm_client.geometry import SMMLine, SMMPoi, SMMPolygon
from smm_client.organizations import SMMOrganization
from smm_client.types import SMMMissingKeyError, SMMParseError


def _parse_geometry_pk(result: requests.Response, context: str) -> int | None:
    if result.status_code != requests.codes["ok"]:
        return None
    try:
        return result.json()["features"][0]["properties"]["pk"]
    except (ValueError, KeyError, IndexError) as exc:
        raise SMMParseError(context, exc) from exc


if TYPE_CHECKING:
    from smm_client.assets import SMMAsset
    from smm_client.connection import SMMConnection, SMMUser
    from smm_client.types import SMMPoint


class SMMMissionAssetStatusValue:
    # pylint: disable=R0903
    """
    Search Management Map - Mission Asset Status Value
    """

    def __init__(self, value_id: int, name: str, description: str) -> None:
        self.id = value_id
        self.name = name
        self.description = description


class SMMMissionOrganization:
    """
    Search Management Map - Organization membership of a Mission
    """

    def __init__(self, mission: SMMMission, organization: SMMOrganization) -> None:
        self.mission = mission
        self.organization = organization

    def set_can_add_organizations(self, *, value: bool) -> bool:
        """
        Set whether this organization can add organizations or not
        """
        response = self.mission.post(f"organizations/{self.organization.id}/", {"add_organization": value})
        return response.status_code == requests.codes["ok"]

    def set_can_add_users(self, *, value: bool) -> bool:
        """
        Set whether this organization can add members or not
        """
        response = self.mission.post(f"organizations/{self.organization.id}/", {"add_user": value})
        return response.status_code == requests.codes["ok"]


class SMMMissionMember:
    """
    Search Management Map - User membership of a Mission
    """

    def __init__(self, mission: SMMMission, user: SMMUser) -> None:
        self.mission = mission
        self.user = user

    def set_is_admin(self, *, value: bool) -> bool:
        """
        Set whether this user is an admin or not
        Admins have all other permissions as well
        """
        response = self.mission.post(f"users/{self.user.id}/", {"admin": value})
        return response.status_code == requests.codes["ok"]

    def set_can_add_organizations(self, *, value: bool) -> bool:
        """
        Set whether this organization can add organizations or not
        """
        response = self.mission.post(f"users/{self.user.id}/", {"add_organization": value})
        return response.status_code == requests.codes["ok"]

    def set_can_add_users(self, *, value: bool) -> bool:
        """
        Set whether this organization can add members or not
        """
        response = self.mission.post(f"users/{self.user.id}/", {"add_user": value})
        return response.status_code == requests.codes["ok"]


class SMMMissionExternalReference:
    """
    Search Management Map - External Reference for Mission
    """

    def __init__(self, mission: SMMMission, data):
        self.mission = mission
        self.id = data["id"]
        self.name = data["name"]
        self.code = data["code"]
        self.url = data["url"]
        self.notes = data["notes"]

    def delete(self):
        """
        Remove this reference
        """
        self.mission.delete(f"externalreferences/{self.id}/")

    def update(self, name, code, url, notes):
        """
        Update this reference
        """
        self.mission.post(
            f"externalreferences/{self.id}/",
            {
                "name": name,
                "code": code,
                "url": url,
                "notes": notes,
            },
        )


class SMMMission:
    """
    Represents a specific Search and Rescue mission in SMM.
    """

    def __init__(self, connection: SMMConnection, mission_id: int, name: str) -> None:
        """
        Initializes a mission object.

        Args:
            connection (SMMConnection): The connection to the SMM server.
            mission_id (int): The unique ID of the mission.
            name (str): The name of the mission.
        """
        self.connection = connection
        self.id = mission_id
        self.name = name

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    def __url_component(self, page: str) -> str:
        return f"/mission/{self.id}/{page}"

    def post(self, page: str, data: object):
        """
        Performs a POST request to a mission-specific endpoint.

        Args:
            page (str): The endpoint path relative to the mission URL.
            data (object): The data to send in the POST request.
        """
        return self.connection.post(self.__url_component(page), data)

    def get_json(self, page: str):
        """
        Performs a GET request to a mission-specific endpoint and returns JSON.

        Args:
            page (str): The endpoint path relative to the mission URL.

        Returns:
            dict: The parsed JSON response.
        """
        return self.connection.get_json(self.__url_component(page))

    def delete(self, page: str):
        """
        Performs a DELETE request to a mission-specific endpoint.

        Args:
            page (str): The endpoint path relative to the mission URL.
        """
        self.connection.delete(self.__url_component(page))

    def add_member(self, user: SMMUser) -> SMMMissionMember:
        """
        Adds a user as a member of this mission.

        Args:
            user (SMMUser): The user to add.

        Returns:
            SMMMissionMember: The membership object.
        """
        self.post("users/add/", data={"user": user.username})
        return SMMMissionMember(self, user)

    def add_organization(self, organization: SMMOrganization) -> SMMMissionOrganization:
        """
        Adds an organization to this mission.

        Args:
            organization (SMMOrganization): The organization to add.

        Returns:
            SMMMissionOrganization: The organization membership object.
        """
        self.post("organizations/", data={"organization": organization.id})
        return SMMMissionOrganization(self, organization)

    def get_organizations(self) -> list[SMMMissionOrganization]:
        """
        Get all the current organizations in this mission
        """
        data = self.get_json("organizations/")
        if "organizations" not in data:
            raise SMMMissingKeyError("organizations/", "organizations")
        return [
            SMMMissionOrganization(
                self,
                SMMOrganization(
                    self.connection, organization["organization"]["id"], organization["organization"]["name"]
                ),
            )
            for organization in data["organizations"]
        ]

    def add_asset(self, asset: SMMAsset) -> None:
        """
        Add an asset to this mission
        """
        self.post("assets/", data={"asset": asset.id})

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
        self.post("assets/command/set/", data)

    def set_asset_status(self, asset: SMMAsset, status: SMMMissionAssetStatusValue, notes: str) -> None:
        """
        Set the status of a specific asset in the mission
        """
        data = {
            "value_id": status.id,
            "notes": notes,
        }
        self.post(f"assets/{asset.id}/status/", data)

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
        include_removed = str(include == "removed")
        data = self.connection.get_json(self.__url_component(f"assets/?include_removed={include_removed}"))
        if "assets" not in data:
            raise SMMMissingKeyError("assets/", "assets")
        return data["assets"]

    def add_waypoint(self, point: SMMPoint, label: str) -> SMMPoi | None:
        """
        Add a way point to this mission
        """
        results = self.post("data/pois/create/", {"lat": point.lat, "lon": point.lng, "label": label})
        pk = _parse_geometry_pk(results, "mission waypoint")
        return SMMPoi(self, pk) if pk is not None else None

    def _populate_points(self, points: list[SMMPoint], label) -> object:
        """
        Add the points to data
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
        return data

    def add_line(self, points: list[SMMPoint], label: str) -> SMMLine | None:
        """
        Add a line to this mission
        """
        data = self._populate_points(points, label)
        results = self.post("data/userlines/create/", data)
        pk = _parse_geometry_pk(results, "mission line")
        return SMMLine(self, pk) if pk is not None else None

    def add_polygon(self, points: list[SMMPoint], label: str) -> SMMPolygon | None:
        """
        Add a polygon to this mission
        """
        data = self._populate_points(points, label)
        results = self.post("data/userpolygons/create/", data)
        pk = _parse_geometry_pk(results, "mission polygon")
        return SMMPolygon(self, pk) if pk is not None else None

    @classmethod
    def get_mission_for_asset(cls, asset: SMMAsset) -> SMMMission | None:
        """
        Get the current mission for the asset
        """
        data = asset.get_asset_data()
        try:
            return SMMMission(asset.connection, data["mission_id"], data["mission_name"])
        except KeyError:
            return None

    def get_external_references(self) -> list[SMMMissionExternalReference]:
        """
        Get all external references for this mission
        """
        extref_json = self.get_json("externalreferences/")
        return [
            SMMMissionExternalReference(
                self,
                extref,
            )
            for extref in extref_json["external_references"]
        ]

    def add_external_reference(self, name: str, code: str | None, url: str | None, notes: str | None):
        """
        Add an external reference to this mission
        """
        self.post(
            "externalreferences/",
            {
                "name": name,
                "code": code,
                "url": url,
                "notes": notes,
            },
        )

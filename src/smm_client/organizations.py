# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Organizations
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from smm_client.assets import SMMAsset

if TYPE_CHECKING:
    from smm_client.connection import SMMUser


class SMMOrganizationUser:
    # pylint: disable=R0903
    """
    Search Management Map - User in an Organization
    """

    def __init__(
        self, organization: SMMOrganization, username: str, role: str, added, added_by, removed, removed_by
    ) -> None:
        # pylint: disable=R0913, R0917
        self.organization = organization
        self.username = username
        self.role = role
        self.added = added
        self.added_by = added_by
        self.removed = removed
        self.removed_by = removed_by

    def __str__(self) -> str:
        return f"{self.username} ({self.role}) in {self.organization}"


class SMMOrganizationAsset:
    # pylint: disable=R0903
    """
    Search Management Map - Asset in an Organization
    """

    def __init__(self, organization: SMMOrganization, asset: SMMAsset, added, added_by, removed, removed_by) -> None:
        # pylint: disable=R0913, R0917
        self.organization = organization
        self.asset = asset
        self.added = added
        self.added_by = added_by
        self.removed = removed
        self.removed_by = removed_by

    def __str__(self) -> str:
        return f"{self.asset} in {self.organization}"


class SMMOrganization:
    """
    Search Management Map - Organization
    """

    def __init__(self, connection, org_id: int, name: str) -> None:
        self.connection = connection
        self.id = org_id
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __url_component(self, page: str) -> str:
        return f"/organization/{self.id}/{page}"

    def get_members(self) -> list[SMMOrganizationUser]:
        """
        Get all the members of this organization
        """
        organization = self.connection.get_json(self.__url_component(""))
        return [
            SMMOrganizationUser(
                self,
                member_json["user"],
                member_json["role"],
                member_json["added"],
                member_json["added_by"],
                member_json["removed"],
                member_json["removed_by"],
            )
            for member_json in organization["members"]
        ]

    def add_member(self, user: SMMUser, role: str = "M") -> None:
        """
        Add a new member (or update an existing members role)
        """
        self.connection.post(self.__url_component(f"user/{user.username}/"), data={"role": role})

    def remove_member(self, user: SMMUser) -> None:
        """
        Remove a member from this organization
        """
        self.connection.delete(self.__url_component(f"user/{user.username}/"))

    def get_assets(self) -> list[SMMOrganizationAsset]:
        """
        Get all the assets in this organization
        """
        assets_json = self.connection.get_json(self.__url_component("assets/"))["assets"]
        return [
            SMMOrganizationAsset(
                self,
                SMMAsset(self.connection, asset_json["asset"]["id"], asset_json["asset"]["name"]),
                asset_json["added"],
                asset_json["added_by"],
                asset_json["removed"],
                asset_json["removed_by"],
            )
            for asset_json in assets_json
        ]

    def add_asset(self, asset: SMMAsset) -> None:
        """
        Add an asset to this organization
        """
        self.connection.post(self.__url_component(f"assets/{asset.id}/"))

    def remove_asset(self, asset: SMMAsset) -> None:
        """
        Remove an asset from this organization
        """
        self.connection.delete(self.__url_component(f"assets/{asset.id}/"))

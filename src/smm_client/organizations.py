# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Organizations
"""

from __future__ import annotations

from smm_client.assets import SMMAsset


class SMMOrganizationAsset:
    """
    Search Management Map - Asset in an Organization
    """

    def __init__(self, organization: SMMOrganization, asset: SMMAsset, added, added_by, removed, removed_by):
        self.organization = organization
        self.asset = asset
        self.added = added
        self.added_by = added_by
        self.removed = removed
        self.removed_by = removed_by

    def __str__(self):
        return f"{self.asset} in {self.organization}"


class SMMOrganization:
    """
    Search Management Map - Organization
    """

    def __init__(self, connection, org_id: int, name: str):
        self.connection = connection
        self.id = org_id
        self.name = name

    def __str__(self):
        return self.name

    def url_component(self, page: str):
        return f"/organization/{self.id}/{page}"

    def add_member(self, username: str, role: str = "M"):
        self.connection.post(self.url_component(f"user/{username}/"), data={"role": role})

    def remove_member(self, username: str):
        self.connection.delete(self.url_component(f"user/{username}/"))

    def get_assets(self) -> list[SMMOrganizationAsset]:
        assets_json = self.connection.get_json(self.url_component("assets/"))["assets"]
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

    def add_asset(self, asset: SMMAsset):
        self.connection.post(self.url_component(f"assets/{asset.id}/"))

    def remove_asset(self, asset: SMMAsset):
        self.connection.delete(self.url_component(f"assets/{asset.id}/"))

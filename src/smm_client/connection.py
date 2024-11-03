# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map Connection Handlers
"""

from __future__ import annotations

import requests

from smm_client.assets import SMMAsset, SMMAssetType
from smm_client.missions import SMMMission
from smm_client.organizations import SMMOrganization


# pylint: disable = R0903
class SMMUser:
    """
    User in Search Management Map
    """

    def __init__(self, user_id: int, username: str) -> None:
        self.id = user_id
        self.username = username


class SMMConnection:
    """
    Create a connection to the Search Management Map Server
    """

    def __init__(self, url: str, username: str, password: str) -> None:
        self.base_url = url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.login()

    def get(self, path=None) -> requests.Response:
        """
        GET path on this connection
        """
        url = f"{self.base_url}/{path}" if path else self.base_url
        return self.session.get(url)

    def get_json(self, path: str):
        """
        GET json from path on this connection
        """
        url = f"{self.base_url}/{path}"
        return self.session.get(url, headers={"Accept": "application/json"}).json()

    def post(self, path: str, data=None) -> requests.Response:
        """
        POST data to path on this connection
        """
        url = f"{self.base_url}/{path}"
        return self.session.post(url, data=data, headers={"X-CSRFToken": self.session.cookies["csrftoken"]})

    def delete(self, path: str) -> requests.Response:
        """
        DELETE path on this connection
        """
        url = f"{self.base_url}/{path}"
        return self.session.delete(url, headers={"X-CSRFToken": self.session.cookies["csrftoken"]})

    def login(self) -> None:
        """
        Login to the server
        """
        self.get()
        self.post("/accounts/login/", data={"username": self.username, "password": self.password})

    def get_assets(self) -> list[SMMAsset]:
        """
        Get all the assests associated with the logged in user
        """
        assets_json = self.get_json("/assets/")["assets"]
        return [SMMAsset(self, asset_json["id"], asset_json["name"]) for asset_json in assets_json]

    def get_missions(self, only: str = "all") -> list[SMMMission]:
        """
        Get all the missions the logged in user is a member of
        """
        missions_json = self.get_json(f"/mission/list/?only={only}")["missions"]
        return [SMMMission(self, mission_json["id"], mission_json["name"]) for mission_json in missions_json]

    def get_asset_types(self) -> list[SMMAssetType]:
        """
        Get all asset types
        """
        asset_types_json = self.get_json("/assets/assettypes/")["asset_types"]
        return [
            SMMAssetType(self, asset_type_json["id"], asset_type_json["name"]) for asset_type_json in asset_types_json
        ]

    def get_organizations(self, *, all_orgs=False) -> list[SMMOrganization]:
        """
        Get all Organizations
        """
        url = "/organization/" if all_orgs else "/organization/?only=mine"
        organizations_json = self.get_json(url)["organizations"]
        return [
            SMMOrganization(self, organization_json["id"], organization_json["name"])
            for organization_json in organizations_json
        ]

    def create_user(self, username: str, password: str) -> SMMUser:
        """
        Add a new user to this server
        """
        result = self.post(
            "/admin/auth/user/add/",
            {"username": username, "password1": password, "password2": password, "_save": "Save"},
        )
        url_parts = result.url.split("/")
        return SMMUser(url_parts[-3], username)

    def create_asset_type(self, asset_type: str, description: str) -> SMMAssetType:
        """
        Create a new asset type
        """
        result = self.post(
            "/admin/assets/assettype/add/",
            {"name": asset_type, "description": description, "_continue": "Save+and+continue+editing"},
        )
        url_parts = result.url.split("/")
        return SMMAssetType(self, url_parts[-3], asset_type)

    def create_asset(self, user: SMMUser, asset: str, asset_type: SMMAssetType) -> SMMAsset:
        """
        Create a new asset
        """
        result = self.post(
            "/admin/assets/asset/add/",
            {"name": asset, "owner": user.id, "asset_type": asset_type.id, "_continue": "Save+and+continue+editing"},
        )
        url_parts = result.url.split("/")
        return SMMAsset(self, url_parts[-3], asset)

    def create_mission(self, name: str, description: str) -> SMMMission | None:
        """
        Create a new mission
        """
        res = self.post("/mission/new/", {"mission_name": name, "mission_description": description})
        if res.status_code == requests.codes["ok"]:
            return SMMMission(self, res.url.split("/")[-3], name)
        return None

    def create_organization(self, name: str) -> SMMOrganization:
        """
        Create a new organization
        """
        org_json = self.post("/organization/", {"name": name}).json()
        return SMMOrganization(self, org_json["id"], org_json["name"])

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


class SMMConnection:
    """
    Create a connection to the Search Management Map Server
    """

    def __init__(self, url: str, username: str, password: str):
        self.base_url = url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.login()

    def get(self, path=None):
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

    def post(self, path: str, data=None):
        """
        POST data to path on this connection
        """
        url = f"{self.base_url}/{path}"
        return self.session.post(url, data=data, headers={"X-CSRFToken": self.session.cookies["csrftoken"]})

    def delete(self, path: str):
        """
        DELETE path on this connection
        """
        url = f"{self.base_url}/{path}"
        return self.session.delete(url, headers={"X-CSRFToken": self.session.cookies["csrftoken"]})

    def login(self):
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

    def create_user(self, username : str, password : str):
        """
        Add a new user to this server
        """
        self.post(
            "/admin/auth/user/add/",
            {"username": username, "password1": password, "password2": password, "_save": "Save"},
        )

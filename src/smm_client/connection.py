# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map Connection Handlers
"""

from __future__ import annotations

import requests

from smm_client.assets import SMMAsset, SMMAssetStatusValue, SMMAssetType
from smm_client.missions import SMMMission, SMMMissionAssetStatusValue
from smm_client.organizations import SMMOrganization
from smm_client.types import (
    SMMCSRFTokenError,
    SMMDeleteCSRFError,
    SMMDeleteHTTPError,
    SMMGetHTTPError,
    SMMJSONDecodeError,
    SMMLoginNoSessionError,
    SMMMissingKeyError,
    SMMParseError,
    SMMPostCSRFError,
    SMMPostHTTPError,
    SMMUnexpectedRedirectError,
)

_MIN_REDIRECT_URL_PARTS = 3


def _parse_redirect_id(resource: str, url: str) -> str:
    url_parts = url.split("/")
    if len(url_parts) < _MIN_REDIRECT_URL_PARTS:
        raise SMMUnexpectedRedirectError(resource, url)
    return url_parts[-_MIN_REDIRECT_URL_PARTS]


# pylint: disable = R0903
class SMMUser:
    """
    User in Search Management Map
    """

    def __init__(self, user_id: int, username: str) -> None:
        self.id = user_id
        self.username = username


class SMMConnection:
    # pylint: disable=R0904
    """
    Manages the connection and authentication to a Search Management Map (SMM) server.
    """

    def __init__(self, url: str, username: str, password: str) -> None:
        """
        Initializes the connection and logs in to the SMM server.

        Args:
            url (str): The base URL of the SMM server.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        self.base_url = url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.login()

    def get(self, path=None) -> requests.Response:
        """
        Performs a GET request to the specified path.

        Args:
            path (str, optional): The path to request, relative to the base URL.

        Returns:
            requests.Response: The response from the server.
        """
        url = f"{self.base_url}/{path}" if path else self.base_url
        return self.session.get(url)

    def get_json(self, path: str):
        """
        Performs a GET request and returns the parsed JSON response.

        Args:
            path (str): The path to request, relative to the base URL.

        Returns:
            dict: The parsed JSON response.

        Raises:
            SMMRequestError: If the request fails or returns non-JSON content.
        """
        url = f"{self.base_url}/{path}"
        response = self.session.get(url, headers={"Accept": "application/json"})
        try:
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as exc:
            raise SMMGetHTTPError(path, exc) from exc
        except ValueError as exc:
            raise SMMJSONDecodeError(path, exc) from exc

    def post(self, path: str, data=None) -> requests.Response:
        """
        Performs a POST request to the specified path.

        Args:
            path (str): The path to request, relative to the base URL.
            data (dict, optional): The data to send in the POST request.

        Returns:
            requests.Response: The response from the server.

        Raises:
            SMMRequestError: If the request fails or CSRF token is missing.
        """
        if "csrftoken" not in self.session.cookies:
            raise SMMPostCSRFError

        url = f"{self.base_url}/{path}"
        response = self.session.post(url, data=data, headers={"X-CSRFToken": self.session.cookies["csrftoken"]})
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise SMMPostHTTPError(path, exc) from exc
        return response

    def delete(self, path: str) -> requests.Response:
        """
        Performs a DELETE request to the specified path.

        Args:
            path (str): The path to request, relative to the base URL.

        Returns:
            requests.Response: The response from the server.

        Raises:
            SMMRequestError: If the request fails or CSRF token is missing.
        """
        if "csrftoken" not in self.session.cookies:
            raise SMMDeleteCSRFError

        url = f"{self.base_url}/{path}"
        response = self.session.delete(url, headers={"X-CSRFToken": self.session.cookies["csrftoken"]})
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise SMMDeleteHTTPError(path, exc) from exc
        return response

    def login(self) -> None:
        """
        Authenticates with the SMM server using the provided credentials.
        """
        self.get()
        if "csrftoken" not in self.session.cookies:
            raise SMMCSRFTokenError

        self.post("/accounts/login/", data={"username": self.username, "password": self.password})

        # Any non-2xx response is already raised by post() as SMMPostHTTPError.
        # We verify a session cookie was established to confirm authentication succeeded.
        if "sessionid" not in self.session.cookies:
            raise SMMLoginNoSessionError

    def get_assets(self) -> list[SMMAsset]:
        """
        Retrieves all assets associated with the authenticated user.

        Returns:
            list[SMMAsset]: A list of SMMAsset objects.
        """
        data = self.get_json("/assets/")
        if "assets" not in data:
            raise SMMMissingKeyError("/assets/", "assets")
        assets_json = data["assets"]
        return [SMMAsset(self, asset_json["id"], asset_json["name"]) for asset_json in assets_json]

    def get_missions(self, only: str = "all") -> list[SMMMission]:
        """
        Retrieves missions the authenticated user is a member of.

        Args:
            only (str): Filter for missions (e.g., 'all', 'active'). Defaults to 'all'.

        Returns:
            list[SMMMission]: A list of SMMMission objects.
        """
        data = self.get_json(f"/mission/list/?only={only}")
        if "missions" not in data:
            raise SMMMissingKeyError(f"/mission/list/?only={only}", "missions")
        missions_json = data["missions"]
        return [SMMMission(self, mission_json["id"], mission_json["name"]) for mission_json in missions_json]

    def get_asset_types(self) -> list[SMMAssetType]:
        """
        Get all asset types
        """
        data = self.get_json("/assets/assettypes/")
        if "asset_types" not in data:
            raise SMMMissingKeyError("/assets/assettypes/", "asset_types")
        asset_types_json = data["asset_types"]
        return [
            SMMAssetType(self, asset_type_json["id"], asset_type_json["name"]) for asset_type_json in asset_types_json
        ]

    def create_asset_status_value(self, name: str, description: str, *, inop: bool) -> SMMAssetStatusValue:
        """
        Add an asset status value
        """
        result = self.post(
            "/admin/assets/assetstatusvalue/add/",
            {"name": name, "description": description, "inop": inop, "_continue": "Save+and+continue+editing"},
        )
        return SMMAssetStatusValue(_parse_redirect_id("asset status value", result.url), name, description, inop=inop)

    def get_asset_status_values(self) -> list[SMMAssetStatusValue]:
        """
        Get all the asset status values
        """
        data = self.get_json("/assets/status/values/")
        if "values" not in data:
            raise SMMMissingKeyError("/assets/status/values/", "values")
        asset_status_values_json = data["values"]
        return [
            SMMAssetStatusValue(
                asset_status_value["id"],
                asset_status_value["name"],
                asset_status_value["description"],
                inop=asset_status_value["inop"],
            )
            for asset_status_value in asset_status_values_json
        ]

    def get_or_create_asset_status_value(self, name: str, description: str, *, inop: bool) -> SMMAssetStatusValue:
        """
        Get the asset status value that matches this name
        Otherwise create it
        """
        status_values = self.get_asset_status_values()
        for sv in status_values:
            if sv.name == name:
                return sv
        return self.create_asset_status_value(name, description, inop=inop)

    def create_mission_asset_status_value(self, name: str, description: str) -> SMMMissionAssetStatusValue:
        """
        Add a mission asset status value
        """
        result = self.post(
            "/admin/mission/missionassetstatusvalue/add/",
            {"name": name, "description": description, "_continue": "Save+and+continue+editing"},
        )
        return SMMMissionAssetStatusValue(_parse_redirect_id("mission asset status value", result.url), name, description)

    def get_mission_asset_status_values(self) -> list[SMMMissionAssetStatusValue]:
        """
        Get all the mission asset status values
        """
        data = self.get_json("/mission/asset/status/values/")
        if "values" not in data:
            raise SMMMissingKeyError("/mission/asset/status/values/", "values")
        mission_asset_status_values_json = data["values"]
        return [
            SMMMissionAssetStatusValue(
                asset_status_value["id"], asset_status_value["name"], asset_status_value["description"]
            )
            for asset_status_value in mission_asset_status_values_json
        ]

    def get_or_create_mission_asset_status_value(self, name: str, description: str) -> SMMMissionAssetStatusValue:
        """
        Get the mission asset status value that matches this name
        Otherwise create it
        """
        status_values = self.get_mission_asset_status_values()
        for sv in status_values:
            if sv.name == name:
                return sv
        return self.create_mission_asset_status_value(name, description)

    def get_organizations(self, *, all_orgs=False) -> list[SMMOrganization]:
        """
        Get all Organizations
        """
        url = "/organization/" if all_orgs else "/organization/?only=mine"
        data = self.get_json(url)
        if "organizations" not in data:
            raise SMMMissingKeyError(url, "organizations")
        organizations_json = data["organizations"]
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
        return SMMUser(_parse_redirect_id("user", result.url), username)

    def create_asset_type(self, asset_type: str, description: str) -> SMMAssetType:
        """
        Create a new asset type
        """
        result = self.post(
            "/admin/assets/assettype/add/",
            {"name": asset_type, "description": description, "_continue": "Save+and+continue+editing"},
        )
        return SMMAssetType(self, _parse_redirect_id("asset type", result.url), asset_type)

    def get_or_create_asset_type(self, asset_type: str, description: str) -> SMMAssetType:
        """
        Get the asset type that matches this asset type
        Otherwise create it
        """
        asset_types = self.get_asset_types()
        for at in asset_types:
            if at.name == asset_type:
                return at
        return self.create_asset_type(asset_type, description)

    def create_asset(self, user: SMMUser, asset: str, asset_type: SMMAssetType) -> SMMAsset:
        """
        Create a new asset
        """
        result = self.post(
            "/admin/assets/asset/add/",
            {"name": asset, "owner": user.id, "asset_type": asset_type.id, "_continue": "Save+and+continue+editing"},
        )
        return SMMAsset(self, _parse_redirect_id("asset", result.url), asset)

    def create_mission(self, name: str, description: str) -> SMMMission | None:
        """
        Create a new mission
        """
        res = self.post("/mission/new/", {"mission_name": name, "mission_description": description})
        if res.status_code == requests.codes["ok"]:
            return SMMMission(self, _parse_redirect_id("mission", res.url), name)
        return None

    def create_organization(self, name: str) -> SMMOrganization:
        """
        Create a new organization
        """
        res = self.post("/organization/", {"name": name})
        try:
            org_json = res.json()
            return SMMOrganization(self, org_json["id"], org_json["name"])
        except (ValueError, KeyError) as exc:
            raise SMMParseError("organization", exc) from exc

    def get_or_create_organization(self, name: str) -> SMMOrganization:
        """
        Get the organization that matches name
        Will be created if it doesn't already exist
        """
        organizations = self.get_organizations()
        for org in organizations:
            if org.name == name:
                return org
        return self.create_organization(name)

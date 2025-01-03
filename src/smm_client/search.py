# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Search
"""

from __future__ import annotations

from json import JSONDecodeError
from typing import TYPE_CHECKING

from smm_client.types import SMMPoint

if TYPE_CHECKING:
    from smm_client.assets import SMMAsset
    from smm_client.connection import SMMConnection


class SMMSearchData:
    # pylint: disable=R0903
    """
    Data for a specific search
    """

    def __init__(self, geojson):
        self.id = geojson["id"]
        self.properties = geojson["properties"]
        self.coords = [SMMPoint(p[1], p[0]) for p in geojson["geometry"]["coordinates"]]


class SMMSearch:
    """
    Base class for searches
    """

    def __init__(self, connection: SMMConnection, search_id: int):
        self.connection = connection
        self.id = search_id

    def __url_component(self, page: str | None) -> str:
        return f"/search/{self.id}/{page}" if page else f"/search/{self.id}/"

    def get_data(self) -> SMMSearchData | None:
        """
        Get the data for this search
        """
        res = self.connection.get_json(self.__url_component(None))
        try:
            return SMMSearchData(res.json()["features"][0])
        except JSONDecodeError:
            return None

    def queue(self, asset: SMMAsset | None) -> bool:
        """
        Queue this search for a specific asset, or just for the asset type
        """
        if asset is not None:
            res = self.connection.post(self.__url_component("queue/"), data={"asset": asset.id})
        else:
            res = self.connection.post(self.__url_component("queue/"))
        return res.text == "Success"

    def begin(self, asset: SMMAsset) -> SMMSearchData | None:
        """
        Begin this search with asset
        """
        res = self.connection.post(self.__url_component("begin/"), data={"asset_id": asset.id})
        try:
            return SMMSearchData(res.json()["features"][0])
        except JSONDecodeError:
            return None

    def finished(self, asset: SMMAsset) -> bool:
        """
        Mark this search as finished/completed by asset
        """
        res = self.connection.post(self.__url_component("finished/"), data={"asset_id": asset.id})
        return res.text == "Completed"

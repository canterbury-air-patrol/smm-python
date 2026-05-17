# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Geometry
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from smm_client.types import SMMParseError

if TYPE_CHECKING:
    from smm_client.assets import SMMAssetType
    from smm_client.missions import SMMMission


def _parse_features_pk(result: requests.Response, context: str) -> int | None:
    if result.status_code != requests.codes["ok"]:
        return None
    try:
        return result.json()["features"][0]["properties"]["pk"]
    except (ValueError, KeyError, IndexError) as exc:
        raise SMMParseError(context, exc) from exc


# pylint: disable=R0903
class SMMGeometry:
    """
    Search Management Map - Parent class for user geometry
    """

    def __init__(self, mission: SMMMission, geo_id: int) -> None:
        self.connection = mission.connection
        self.mission = mission
        self.geo_id = geo_id


class SMMPoi(SMMGeometry):
    """
    Search Management Map - Point of Interest
    """

    def create_sector_search(self, sweep_width: int, asset_type: SMMAssetType) -> int | None:
        """
        Create a sector search starting at this POI
        """
        result = self.connection.post(
            "search/sector/create/",
            data={"poi_id": self.geo_id, "asset_type_id": asset_type.id, "sweep_width": sweep_width},
        )
        return _parse_features_pk(result, "sector search")

    def create_expanding_box_search(
        self, sweep_width: int, asset_type: SMMAssetType, iterations: int, first_bearing: int = 0
    ) -> int | None:
        """
        Create an expanding box search starting at this POI
        """
        result = self.connection.post(
            "search/expandingbox/create/",
            data={
                "poi_id": self.geo_id,
                "asset_type_id": asset_type.id,
                "sweep_width": sweep_width,
                "iterations": iterations,
                "first_bearing": first_bearing,
            },
        )
        return _parse_features_pk(result, "expanding box search")


class SMMLine(SMMGeometry):
    """
    Search Management Map - Line
    """

    def create_shoreline_search(self, sweep_width: int, asset_type: SMMAssetType) -> int | None:
        """
        Create a shoreline search along this line
        """
        result = self.connection.post(
            "search/shoreline/create/",
            data={"poi_id": self.geo_id, "asset_type_id": asset_type.id, "sweep_width": sweep_width},
        )
        return _parse_features_pk(result, "shoreline search")

    def create_trackline_search(self, sweep_width: int, asset_type: SMMAssetType) -> int | None:
        """
        Create a trackline search along this line
        """
        result = self.connection.post(
            "search/trackline/create/",
            data={"poi_id": self.geo_id, "asset_type_id": asset_type.id, "sweep_width": sweep_width},
        )
        return _parse_features_pk(result, "trackline search")

    def create_creepingline_search(self, sweep_width: int, asset_type: SMMAssetType, width: int) -> int | None:
        """
        Create a creeping line ahead search along this line
        """
        result = self.connection.post(
            "search/creepingline/create/track/",
            data={"poi_id": self.geo_id, "asset_type_id": asset_type.id, "sweep_width": sweep_width, "width": width},
        )
        return _parse_features_pk(result, "creeping line search")


class SMMPolygon(SMMGeometry):
    """
    Search Management Map -- Polygon
    """

    def create_creepingline_search(self, sweep_width: int, asset_type: SMMAssetType) -> int | None:
        """
        Create a creeping line ahead search inside this polygon
        """
        result = self.connection.post(
            "search/creepingline/create/polygon/",
            data={"poi_id": self.geo_id, "asset_type_id": asset_type.id, "sweep_width": sweep_width},
        )
        return _parse_features_pk(result, "polygon creeping line search")

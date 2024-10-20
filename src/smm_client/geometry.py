# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Geometry
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from smm_client.assets import SMMAssetType
    from smm_client.missions import SMMMission


# pylint: disable=R0903
class SMMGeometry:
    """
    Search Management Map - Parent class for user geometry
    """

    def __init__(self, mission: SMMMission, geo_id: int):
        self.connection = mission.connection
        self.mission = mission
        self.geo_id = geo_id


class SMMPoi(SMMGeometry):
    """
    Search Management Map - Point of Interest
    """

    def create_sector_search(self, sweep_width: int, asset_type: SMMAssetType):
        """
        Create a sector search starting at this POI
        """
        result = self.connection.post(
            "search/sector/create/",
            data={"poi_id": self.geo_id, "asset_type_id": asset_type.id, "sweep_width": sweep_width},
        )
        if result.status_code == requests.codes["ok"]:
            json_obj = result.json()
            return json_obj["features"][0]["properties"]["pk"]
        return None

    def create_expanding_box_search(
        self, sweep_width: int, asset_type: SMMAssetType, iterations: int, first_bearing: int = 0
    ):
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
        if result.status_code == requests.codes["ok"]:
            json_obj = result.json()
            return json_obj["features"][0]["properties"]["pk"]
        return None

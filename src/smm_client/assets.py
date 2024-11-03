# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Assets
"""


class SMMAsset:
    # pylint: disable=R0903
    """
    Search Management Map - Asset
    """

    def __init__(self, connection, asset_id: int, name: str) -> None:
        self.connection = connection
        self.id = asset_id
        self.name = name

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

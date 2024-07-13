# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Missions
"""


class SMMMission:
    """
    Search Management Map - Mission
    """

    def __init__(self, connection, mission_id: int, name: str):
        self.connection = connection
        self.id = mission_id
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.id})"

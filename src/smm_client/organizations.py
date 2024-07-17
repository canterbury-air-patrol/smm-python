# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Organizations
"""


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

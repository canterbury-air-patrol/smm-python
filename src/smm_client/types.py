# SPDX-FileCopyrightText: 2024-present Canterbury Air Patrol Inc <github@canterburyairpatrol.org>
#
# SPDX-License-Identifier: MIT
"""
Search Management Map - Types
"""

MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0


class LatitudeError(ValueError):
    def __init__(self):
        super().__init__(f"Latitude out of range ({MIN_LATITUDE}, {MAX_LATITUDE} degrees)")


class LongitudeError(ValueError):
    def __init__(self):
        super().__init__(f"Longitude out of range ({MIN_LONGITUDE}, {MAX_LONGITUDE} degrees)")


class SMMPoint:
    """
    Latitude/Longitude combination
    """

    def __init__(self, latitude: float, longitude: float):
        self.lat = latitude
        self.lng = longitude

    def set_lat(self, lat: float):
        if lat < MIN_LATITUDE or lat > MAX_LATITUDE:
            raise LatitudeError
        self._lat = lat

    def get_lat(self) -> float:
        return self._lat

    def set_lng(self, lng: float):
        if lng < MIN_LONGITUDE or lng > MAX_LONGITUDE:
            raise LongitudeError
        self._lng = lng

    def get_lng(self) -> float:
        return self._lng

    lat = property(get_lat, set_lat)
    latitude = property(get_lat, set_lat)
    lng = property(get_lng, set_lng)
    longitude = property(get_lng, set_lng)

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
    """
    Class for errors with latitudes
    """

    def __init__(self) -> None:
        super().__init__(f"Latitude out of range ({MIN_LATITUDE}, {MAX_LATITUDE} degrees)")


class LongitudeError(ValueError):
    """
    Class for errors with longitude
    """

    def __init__(self) -> None:
        super().__init__(f"Longitude out of range ({MIN_LONGITUDE}, {MAX_LONGITUDE} degrees)")


class SMMError(Exception):
    """
    Base class for exceptions in this module.
    """


class SMMAuthenticationError(SMMError):
    """
    Exception raised for authentication errors.
    """


class SMMCSRFTokenError(SMMAuthenticationError):
    """
    Exception raised when a CSRF token cannot be obtained from the server.
    """

    def __init__(self) -> None:
        super().__init__("Failed to obtain CSRF token from server")


class SMMLoginHTTPError(SMMAuthenticationError):
    """
    Exception raised when login fails with a non-OK HTTP status code.
    """

    def __init__(self, status_code: int) -> None:
        super().__init__(f"Login failed with status code: {status_code}")


class SMMLoginNoSessionError(SMMAuthenticationError):
    """
    Exception raised when login succeeds HTTP-wise but no session ID is received.
    """

    def __init__(self) -> None:
        super().__init__("Login failed: No session ID received")


class SMMRequestError(SMMError):
    """
    Exception raised for errors during a request to the SMM server.
    """


class SMMGetHTTPError(SMMRequestError):
    """
    Exception raised when an HTTP GET request fails.
    """

    def __init__(self, path: str, exc: Exception) -> None:
        super().__init__(f"HTTP error during GET {path}: {exc}")


class SMMJSONDecodeError(SMMRequestError):
    """
    Exception raised when a JSON response cannot be decoded.
    """

    def __init__(self, path: str, exc: Exception) -> None:
        super().__init__(f"Failed to decode JSON response from {path}: {exc}")


class SMMPoint:
    # pylint: disable=R0903
    """
    Latitude/Longitude combination
    """

    def __init__(self, latitude: float, longitude: float) -> None:
        self._lat = None
        self._lng = None
        self.lat = latitude
        self.lng = longitude

    def __set_lat(self, lat: float) -> None:
        if lat < MIN_LATITUDE or lat > MAX_LATITUDE:
            raise LatitudeError
        self._lat = lat

    def __get_lat(self) -> float:
        """
        Get the latitude
        """
        return self._lat

    def __set_lng(self, lng: float) -> None:
        if lng < MIN_LONGITUDE or lng > MAX_LONGITUDE:
            raise LongitudeError
        self._lng = lng

    def __get_lng(self) -> float:
        return self._lng

    lat = property(__get_lat, __set_lat)
    latitude = property(__get_lat, __set_lat)
    lng = property(__get_lng, __set_lng)
    longitude = property(__get_lng, __set_lng)

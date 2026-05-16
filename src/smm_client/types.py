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


class SMMPostCSRFError(SMMRequestError):
    """
    Exception raised when a POST request cannot be made due to a missing CSRF token.
    """

    def __init__(self) -> None:
        super().__init__("Cannot perform POST request: Missing CSRF token. Are you logged in?")


class SMMPostHTTPError(SMMRequestError):
    """
    Exception raised when an HTTP POST request fails.
    """

    def __init__(self, path: str, exc: Exception) -> None:
        super().__init__(f"HTTP error during POST {path}: {exc}")


class SMMDeleteCSRFError(SMMRequestError):
    """
    Exception raised when a DELETE request cannot be made due to a missing CSRF token.
    """

    def __init__(self) -> None:
        super().__init__("Cannot perform DELETE request: Missing CSRF token. Are you logged in?")


class SMMDeleteHTTPError(SMMRequestError):
    """
    Exception raised when an HTTP DELETE request fails.
    """

    def __init__(self, path: str, exc: Exception) -> None:
        super().__init__(f"HTTP error during DELETE {path}: {exc}")


class SMMAssetsKeyError(SMMRequestError):
    """
    Exception raised when the assets response is missing the 'assets' key.
    """

    def __init__(self) -> None:
        super().__init__("Unexpected response format from /assets/: missing 'assets' key")


class SMMMissionsKeyError(SMMRequestError):
    """
    Exception raised when the missions response is missing the 'missions' key.
    """

    def __init__(self) -> None:
        super().__init__("Unexpected response format from /mission/list/: missing 'missions' key")


class SMMAssetTypesKeyError(SMMRequestError):
    """
    Exception raised when the asset types response is missing the 'asset_types' key.
    """

    def __init__(self) -> None:
        super().__init__("Unexpected response format from /assets/assettypes/: missing 'asset_types' key")


class SMMAssetStatusValuesKeyError(SMMRequestError):
    """
    Exception raised when the asset status values response is missing the 'values' key.
    """

    def __init__(self) -> None:
        super().__init__("Unexpected response format from /assets/status/values/: missing 'values' key")


class SMMMissionAssetStatusValuesKeyError(SMMRequestError):
    """
    Exception raised when the mission asset status values response is missing the 'values' key.
    """

    def __init__(self) -> None:
        super().__init__("Unexpected response format from /mission/asset/status/values/: missing 'values' key")


class SMMOrgURLKeyError(SMMRequestError):
    """
    Exception raised when an organization list response is missing the 'organizations' key.
    """

    def __init__(self, url: str) -> None:
        super().__init__(f"Unexpected response format from {url}: missing 'organizations' key")


class SMMMissionOrgsKeyError(SMMRequestError):
    """
    Exception raised when a mission's organization list response is missing the 'organizations' key.
    """

    def __init__(self) -> None:
        super().__init__("Unexpected response format from organizations/: missing 'organizations' key")


class SMMMissionAssetsKeyError(SMMRequestError):
    """
    Exception raised when a mission's asset list response is missing the 'assets' key.
    """

    def __init__(self) -> None:
        super().__init__("Unexpected response format from assets/: missing 'assets' key")


class SMMOrgMembersKeyError(SMMRequestError):
    """
    Exception raised when an organization members response is missing the 'members' key.
    """

    def __init__(self) -> None:
        super().__init__("Unexpected response format from organization/: missing 'members' key")


class SMMOrgAssetsKeyError(SMMRequestError):
    """
    Exception raised when an organization assets response is missing the 'assets' key.
    """

    def __init__(self) -> None:
        super().__init__("Unexpected response format from organization assets/: missing 'assets' key")


class SMMAssetStatusRedirectError(SMMRequestError):
    """
    Exception raised when creating an asset status value returns an unexpected redirect URL.
    """

    def __init__(self, url: str) -> None:
        super().__init__(f"Unexpected redirect URL after creating asset status value: {url}")


class SMMMissionAssetStatusRedirectError(SMMRequestError):
    """
    Exception raised when creating a mission asset status value returns an unexpected redirect URL.
    """

    def __init__(self, url: str) -> None:
        super().__init__(f"Unexpected redirect URL after creating mission asset status value: {url}")


class SMMUserRedirectError(SMMRequestError):
    """
    Exception raised when creating a user returns an unexpected redirect URL.
    """

    def __init__(self, url: str) -> None:
        super().__init__(f"Unexpected redirect URL after creating user: {url}")


class SMMAssetTypeRedirectError(SMMRequestError):
    """
    Exception raised when creating an asset type returns an unexpected redirect URL.
    """

    def __init__(self, url: str) -> None:
        super().__init__(f"Unexpected redirect URL after creating asset type: {url}")


class SMMAssetRedirectError(SMMRequestError):
    """
    Exception raised when creating an asset returns an unexpected redirect URL.
    """

    def __init__(self, url: str) -> None:
        super().__init__(f"Unexpected redirect URL after creating asset: {url}")


class SMMMissionRedirectError(SMMRequestError):
    """
    Exception raised when creating a mission returns an unexpected redirect URL.
    """

    def __init__(self, url: str) -> None:
        super().__init__(f"Unexpected redirect URL after creating mission: {url}")


class SMMOrgParseError(SMMRequestError):
    """
    Exception raised when an organization creation response cannot be parsed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Failed to parse organization creation response: {exc}")


class SMMAssetStatusMalformedError(SMMRequestError):
    """
    Exception raised when asset status data is malformed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Malformed asset status data: missing key {exc}")


class SMMAssetCommandMalformedError(SMMRequestError):
    """
    Exception raised when asset command data is malformed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Malformed asset command data: missing key {exc}")


class SMMOrgMemberMalformedError(SMMRequestError):
    """
    Exception raised when organization member data is malformed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Malformed member data: missing key {exc}")


class SMMOrgAssetMalformedError(SMMRequestError):
    """
    Exception raised when organization asset data is malformed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Malformed organization asset data: missing key {exc}")


class SMMSearchMalformedError(SMMRequestError):
    """
    Exception raised when search data is malformed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Malformed search data: {exc}")


class SMMWaypointParseError(SMMRequestError):
    """
    Exception raised when a waypoint creation response cannot be parsed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Failed to parse waypoint creation response: {exc}")


class SMMLineParseError(SMMRequestError):
    """
    Exception raised when a line creation response cannot be parsed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Failed to parse line creation response: {exc}")


class SMMPolygonParseError(SMMRequestError):
    """
    Exception raised when a polygon creation response cannot be parsed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Failed to parse polygon creation response: {exc}")


class SMMSectorSearchParseError(SMMRequestError):
    """
    Exception raised when a sector search creation response cannot be parsed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Failed to parse sector search creation response: {exc}")


class SMMExpandingBoxSearchParseError(SMMRequestError):
    """
    Exception raised when an expanding box search creation response cannot be parsed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Failed to parse expanding box search creation response: {exc}")


class SMMShorelineSearchParseError(SMMRequestError):
    """
    Exception raised when a shoreline search creation response cannot be parsed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Failed to parse shoreline search creation response: {exc}")


class SMMTracklineSearchParseError(SMMRequestError):
    """
    Exception raised when a trackline search creation response cannot be parsed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Failed to parse trackline search creation response: {exc}")


class SMMCreepingLineSearchParseError(SMMRequestError):
    """
    Exception raised when a creeping line search creation response cannot be parsed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Failed to parse creeping line search creation response: {exc}")


class SMMPolygonCreepingLineSearchParseError(SMMRequestError):
    """
    Exception raised when a polygon creeping line search creation response cannot be parsed.
    """

    def __init__(self, exc: Exception) -> None:
        super().__init__(f"Failed to parse polygon creeping line search creation response: {exc}")


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

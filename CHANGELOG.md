# Changelog

All notable changes to smm-client are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Custom exception hierarchy rooted at `SMMError` for structured error handling.
  Specific types: `SMMAuthenticationError`, `SMMCSRFTokenError`, `SMMLoginNoSessionError`,
  `SMMRequestError`, `SMMGetHTTPError`, `SMMPostHTTPError`, `SMMDeleteHTTPError`,
  `SMMJSONDecodeError`, `SMMMissingKeyError`, `SMMUnexpectedRedirectError`,
  `SMMParseError`, `SMMMalformedDataError`
- Comprehensive error handling across all API methods
- `SMMConnection` and `SMMPoint` exported from the top-level `smm_client` package

### Fixed
- Incorrect URL for trackline search creation
- Empty asset command data no longer raises an exception

## [0.0.16] - 2025-02-16

### Added
- Mission external references: `SMMMissionExternalReference`, `SMMMission.get_external_references()`, `SMMMission.add_external_reference()`
- Python 3.13 support

## [0.0.15] - 2025-01-04

### Added
- `SMMMission.get_mission_for_asset()` — retrieve the current mission for a given asset

## [0.0.14] - 2025-01-03

### Fixed
- JSON response parsing in `SMMSearch.begin()`

## [0.0.13] - 2025-01-03

### Added
- `SMMSearch.get_data()` to retrieve search coordinates and properties as `SMMSearchData`

## [0.0.12] - 2025-01-03

### Fixed
- Correctly extract search ID from server response

## [0.0.11] - 2025-01-03

### Fixed
- Pass connection object to `SMMSearch` on construction

## [0.0.10] - 2025-01-03

### Fixed
- Correct parameter names for the closest-search endpoint

## [0.0.9] - 2025-01-03

### Fixed
- Switch `get_next_search` to use POST as required by the server

## [0.0.8] - 2024-12-31

### Added
- `SMMSearch` class with `queue()`, `begin()`, and `finished()` methods
- `SMMAsset.set_position()` to report GPS position and telemetry
- `SMMAsset.get_next_search()` to find the nearest queued search for an asset

## [0.0.7] - 2024-12-21

### Fixed
- Mission organization list construction

## [0.0.6] - 2024-12-21

### Added
- `SMMMission.get_organizations()` — list organizations attached to a mission
- `SMMMissionAssetStatusValue` — mission-scoped asset status values
- `SMMConnection.get_mission_asset_status_values()`, `create_mission_asset_status_value()`, `get_or_create_mission_asset_status_value()`
- `SMMMission.set_asset_status()` and `SMMMission.set_asset_command()`

## [0.0.5] - 2024-12-14

### Fixed
- Internal f-string cleanup (no behaviour change)

## [0.0.4] - 2024-12-14

### Fixed
- Missing return type annotations on mission methods

## [0.0.3] - 2024-11-30

### Added
- `SMMMissionOrganization` and `SMMMissionMember` objects for typed mission membership
- `SMMConnection.get_or_create_asset_type()` and `get_or_create_organization()`
- `SMMMission.add_polygon()` and `SMMPolygon` geometry type
- `SMMPolygon.create_creepingline_search()`

### Fixed
- `SMMMission.add_line()` now correctly returns an `SMMLine`

## [0.0.2] - 2024-11-03

### Added
- `SMMLine` geometry type with `create_shoreline_search()`, `create_trackline_search()`, `create_creepingline_search()`
- `SMMAsset.get_status()` and `set_status()` for asset status reporting
- `SMMAsset.get_command()` for retrieving the active asset command
- `SMMPoi.create_sector_search()` and `create_expanding_box_search()`
- `SMMMission.assets()` — list assets in a mission
- Typed return objects from `create_asset_type()`, `create_asset()`, `create_user()`
- `SMMPoi` object returned from waypoint/POI creation

## [0.0.1] - 2024-09-14

### Added
- Initial release
- `SMMConnection` — authenticate and communicate with an SMM server
- `SMMMission` — create and manage SAR missions (add members, organizations, assets, waypoints, lines)
- `SMMOrganization` — create and manage organizations (members, assets)
- `SMMAsset` / `SMMAssetType` — asset management
- `SMMPoi` — point of interest creation
- `SMMPoint` — validated latitude/longitude coordinate type

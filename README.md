# smm-client

[![PyPI - Version](https://img.shields.io/pypi/v/smm-client.svg)](https://pypi.org/project/smm-client)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/smm-client.svg)](https://pypi.org/project/smm-client)

Python client library for [Search Management Map (SMM)](https://github.com/canterbury-air-patrol/search-management-map) — a web application for coordinating search and rescue operations.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Error Handling](#error-handling)
- [Assets](#assets)
- [Missions](#missions)
- [Organizations](#organizations)
- [Searches](#searches)
- [License](#license)

---

## Installation

```console
pip install smm-client
```

---

## Quick Start

```python
from smm_client import SMMConnection

smm = SMMConnection(
    url="https://smm.example.com",
    username="your_username",
    password="your_password",
)
```

`SMMConnection.__init__` calls `login()` automatically. On failure it raises one of the exceptions described below.

---

## Error Handling

All exceptions inherit from `SMMError`, so you can catch everything with a single except clause or be specific.

```
SMMError
├── SMMAuthenticationError
│   ├── SMMCSRFTokenError       # server did not return a CSRF cookie
│   └── SMMLoginNoSessionError  # credentials rejected (no session cookie)
└── SMMRequestError
    ├── SMMGetHTTPError         # non-2xx response to a GET
    ├── SMMPostHTTPError        # non-2xx response to a POST
    ├── SMMDeleteHTTPError      # non-2xx response to a DELETE
    ├── SMMPostCSRFError        # POST attempted without a CSRF token
    ├── SMMDeleteCSRFError      # DELETE attempted without a CSRF token
    ├── SMMJSONDecodeError      # response body was not valid JSON
    ├── SMMMissingKeyError      # expected key absent from JSON response
    ├── SMMUnexpectedRedirectError  # resource creation redirect had unexpected URL
    ├── SMMParseError           # could not parse a creation response
    └── SMMMalformedDataError   # server returned structurally invalid data
```

```python
from smm_client import SMMConnection
from smm_client.types import SMMError, SMMAuthenticationError, SMMRequestError

try:
    smm = SMMConnection(url="https://smm.example.com", username="u", password="p")
except SMMAuthenticationError as e:
    print(f"Login failed: {e}")
except SMMRequestError as e:
    print(f"Network or server error: {e}")
except SMMError as e:
    print(f"Unexpected SMM error: {e}")
```

`LatitudeError` and `LongitudeError` (both `ValueError` subclasses) are raised by `SMMPoint` when coordinates are out of range.

---

## Assets

### Listing and creating assets

```python
# List all assets visible to the authenticated user
assets = smm.get_assets()
for asset in assets:
    print(asset)  # "Heli-1 (42)"

# List available asset types
asset_types = smm.get_asset_types()

# Get or create an asset type
asset_type = smm.get_or_create_asset_type("Helicopter", "Rotary-wing aircraft")

# Create a user and an asset (requires admin access)
user = smm.create_user("pilot1", "password123")
asset = smm.create_asset(user, "Heli-1", asset_type)
```

### Asset status

```python
# Read current status
status = asset.get_status()
if status:
    print(status)  # "Status of Heli-1 is 'Active' since 2025-01-01: On site"

# Retrieve available status values, then set one
status_values = smm.get_asset_status_values()
active_sv = smm.get_or_create_asset_status_value("Active", "Asset is operational", inop=False)
asset.set_status(str(active_sv.id), "On site and searching")
```

### Asset position

```python
from smm_client import SMMPoint

asset.set_position(
    lat=-43.5321,
    lon=172.6362,
    fix=1,       # GPS fix quality (0 = no fix, 1 = fix)
    alt=100,     # altitude in metres
    heading=90,  # degrees
)
```

### Asset commands

```python
command = asset.get_command()
if command:
    print(command)  # "Command 'RTB' issued to Heli-1 at 2025-01-01: Return to base"
```

---

## Missions

### Listing and creating missions

```python
# All missions the user belongs to
missions = smm.get_missions()

# Only active missions
active_missions = smm.get_missions(only="active")

# Create a new mission
mission = smm.create_mission("Search for Missing Hiker", "North Woods area")

# Find the current mission for an asset
current = mission.get_mission_for_asset(asset)
```

### Mission members and organizations

```python
# Add a user as a mission member
member = mission.add_member(user)
member.set_is_admin(value=True)
member.set_can_add_users(value=True)

# Add an organization to the mission
org = smm.get_or_create_organization("Canterbury Air Patrol")
mission_org = mission.add_organization(org)
mission_org.set_can_add_organizations(value=False)

# List current organizations in the mission
mission_orgs = mission.get_organizations()
```

### Mission assets

```python
# Add and remove assets
mission.add_asset(asset)
mission.remove_asset(asset)

# List active assets (pass include="removed" to see historical)
asset_list = mission.assets()

# Set a mission-scoped asset status
msv = smm.get_or_create_mission_asset_status_value("Tasked", "Asset has been given a task")
mission.set_asset_status(asset, msv, notes="Searching grid A3")

# Issue a command to an asset
mission.set_asset_command(asset, command="Search", reason="Assigned to grid A3")
```

### Mission geometry

```python
from smm_client import SMMPoint

# Waypoint (point of interest)
poi = mission.add_waypoint(SMMPoint(-43.5, 172.6), label="LKP")

# Line
line = mission.add_line(
    [SMMPoint(-43.50, 172.60), SMMPoint(-43.51, 172.61)],
    label="Route A",
)

# Polygon
polygon = mission.add_polygon(
    [SMMPoint(-43.50, 172.60), SMMPoint(-43.51, 172.60), SMMPoint(-43.51, 172.61)],
    label="Search Area",
)
```

### External references

```python
refs = mission.get_external_references()

mission.add_external_reference(
    name="Incident Report",
    code="IR-2025-001",
    url="https://example.com/ir/2025/001",
    notes="Filed by coordinating agency",
)

refs[0].update(name="Updated Report", code="IR-2025-001-A", url=None, notes=None)
refs[0].delete()
```

### Closing a mission

```python
mission.close()
```

---

## Organizations

```python
# List organizations the user belongs to
my_orgs = smm.get_organizations()

# List all organizations on the server
all_orgs = smm.get_organizations(all_orgs=True)

# Get or create
org = smm.get_or_create_organization("Canterbury Air Patrol")

# Members
members = org.get_members()
org.add_member(user, role="M")   # role: "M" (member) or "A" (admin)
org.remove_member(user)

# Assets
org_assets = org.get_assets()
org.add_asset(asset)
org.remove_asset(asset)
```

---

## Searches

Searches are typically obtained via `asset.get_next_search()` or created from geometry objects.

```python
# Find the nearest search for an asset
search = asset.get_next_search(lat=-43.5321, lon=172.6362)

if search:
    # Queue for this specific asset (or pass None to queue for the asset type)
    search.queue(asset)

    # Begin the search; returns SMMSearchData with coords and properties
    data = search.begin(asset)
    if data:
        print(data.coords)  # list of SMMPoint

    # Mark complete
    search.finished(asset)

# Create searches from geometry
asset_type = smm.get_or_create_asset_type("Helicopter", "Rotary-wing")

if poi:
    poi.create_sector_search(sweep_width=100, asset_type=asset_type)
    poi.create_expanding_box_search(sweep_width=100, asset_type=asset_type, iterations=3)

if line:
    line.create_shoreline_search(sweep_width=50, asset_type=asset_type)
    line.create_trackline_search(sweep_width=50, asset_type=asset_type)
    line.create_creepingline_search(sweep_width=50, asset_type=asset_type, width=500)

if polygon:
    polygon.create_creepingline_search(sweep_width=50, asset_type=asset_type)
```

---

## License

`smm-client` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

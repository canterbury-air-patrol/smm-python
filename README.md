# smm_client

[![PyPI - Version](https://img.shields.io/pypi/v/smm-client.svg)](https://pypi.org/project/smm-client)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/smm-client.svg)](https://pypi.org/project/smm-client)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install smm-client
```

## Usage

### Initialization

To start, you need to create a connection to the Search Management Map server.

```python
from smm_client.connection import SMMConnection

# Initialize connection
smm = SMMConnection(
    url="https://smm.example.com",
    username="your_username",
    password="your_password"
)
```

### Managing Missions

You can list existing missions or create a new one.

```python
# List missions
missions = smm.get_missions()
for mission in missions:
    print(f"Mission: {mission.name} (ID: {mission.id})")

# Create a new mission
new_mission = smm.create_mission("Search for Missing Hiker", "Search in the North Woods")
```

### Tracking Assets

Track and update the status of your assets.

```python
# Get all assets
assets = smm.get_assets()

# Update asset status
asset = assets[0]
asset.set_status("Active", "On site and searching")

# Update asset position
asset.set_position(
    lat=-43.5321,
    lon=172.6362,
    fix=1,      # 1 for GPS fix
    alt=100,    # Altitude in meters
    heading=90  # Heading in degrees
)
```

## License

`smm-client` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

# Python wrapper for API

Full API spec of the API can be found here:

https://airbyte-public-api-docs.s3.us-east-2.amazonaws.com/rapidoc-api-docs.html


## How to use

### Create client

```
from airbyte_python_helper import AirbyteHelper
import os

airbyte_url = os.environ["AIRBYTE_URL"]
airbyte_client_id = os.environ["CLIENT_ID"]
airbyte_client_secret = os.environ["CLIENT_SECRET"]

airbyte_client = AirbyteHelper(
airbyte_url, airbyte_client_id, airbyte_client_secret
)
```

### Destinations

```
wid = airbyte_client.get_first_workspace_id()
print("workspaceId", wid)
print(airbyte_client.list_destinations(wid))

for destination in airbyte_client.list_destinations(wid):
    airbyte_client.delete_destination(destination["destinationId"])

sources = airbyte_client.list_sources(wid)
```

### Sources

```
wid = airbyte_client.get_first_workspace_id()
print("workspaceId", wid)
sources = airbyte_client.list_sources(wid)
print(sources)
for source in sources:
    print(source["sourceId"])
```

### Workspaces

```
workspaces = airbyte_client.list_workspaces()
print(workspaces)
```
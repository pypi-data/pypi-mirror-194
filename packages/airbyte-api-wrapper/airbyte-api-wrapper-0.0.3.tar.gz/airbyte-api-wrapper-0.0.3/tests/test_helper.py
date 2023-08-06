import os
from airbyte_python_helper import AirbyteHelper

airbyte_client = AirbyteHelper(
    os.environ["AIRBYTE_URL"], os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"]
)
wid = airbyte_client.get_first_workspace_id()
print("workspaceId", wid)
print(airbyte_client.list_destinations(wid))

for destination in airbyte_client.list_destinations(wid):
    airbyte_client.delete_destination(destination["destinationId"])

sources = airbyte_client.list_sources(wid)
print(sources)
for source in sources:
    print(source["sourceId"])

print(airbyte_client.get_logs())

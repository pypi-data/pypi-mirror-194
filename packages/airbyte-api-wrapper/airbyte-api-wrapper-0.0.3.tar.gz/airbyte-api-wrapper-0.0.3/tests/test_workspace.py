import os
from airbyte_python_helper import AirbyteHelper

airbyte_client = AirbyteHelper(
    os.environ["AIRBYTE_URL"], os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"]
)

workspace = airbyte_client.create_workspace({
  "email": "user@example.com",
  "anonymousDataCollection": False,
  "name": "Workspace ABC",
  "news": False,
  "securityUpdates": False,
  "notifications": [
    {
      "notificationType": "slack",
      "sendOnSuccess": False,
      "sendOnFailure": False,
      "slackConfiguration": {
        "webhook": "string"
      },
      "customerioConfiguration": {}
    }
  ],
  "displaySetupWizard": False,
  "defaultGeography": "auto",
  "webhookConfigs": [
    {
      "name": "string",
      "authToken": "string",
      "validationUrl": "string"
    }
  ]
})

print(workspace)
print(workspace)
wid = workspace["workspaceId"]
try:
    print("deleted", wid)
    airbyte_client.update_workspace_name(wid, "Workspace 123")
    res = airbyte_client.get_workspace(wid)
    print(res)
except Exception as e:
    print(e)
res = airbyte_client.delete_workspace(wid)
print(res)
print(res)

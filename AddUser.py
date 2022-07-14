import requests
import json

ACCESS_TOKEN="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";

org_name="TestOrg121"

email=input("ENTER EMAIL_ID: ").strip()

headers={
    "Accept":"application/vnd.github+json",
    "Authorization":f"token {ACCESS_TOKEN}"
}

url=f"https://api.github.com/orgs/{org_name}/invitations"

body={
    "email":f"{email}",
    "role":"direct_member"
}

body=json.dumps(body,indent=4)

r=requests.post(url=url,headers=headers,data=body)

print(r.json())

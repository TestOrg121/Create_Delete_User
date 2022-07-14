import requests
import json

ACCESS_TOKEN="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";

org_name="TestOrg121"

username=input("Enter username: ").strip()

headers={
    "Accept":"application/vnd.github+json",
    "Authorization":f"token {ACCESS_TOKEN}"
}

url=f"https://api.github.com/orgs/{org_name}/members/{username}"


r=requests.delete(url=url,headers=headers)
print(r.status_code)

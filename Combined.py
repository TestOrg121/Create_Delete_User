import re
import os
import requests
import json

#regular expression for pattern matching
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


#function to validate email address
def email_is_valid(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False


#function for adding user to coralogix
def addUser_coralogix(email):
    API_KEY="0a25dbe5-02c5-4eee-bdd7-2933f4299cd1"
    cammand=f"./cxctl teamamte delete --api-key {API_KEY} --region eu --id 35963  {email}:user"
    os.system(cammand)

#function for adding user to github
def addUser_github(email):

    ACCESS_TOKEN="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";

    org_name="TestOrg121"

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

    print(r.status_code)
    


email = ${{github.event.inputs.email}}
plateform = ${{github.event.inputs.plateform}}
operation =${{github.event.inputs.operation}}

if email_is_valid(email):
    if operation=="create":
        if plateform=="coralogix":
            addUser_coralogix(email)
        elif plateform=="github":
            addUser_github(email)

        else:
            print("We don't have Script for this plateform Yet!")
        

        

    elif operation=="delete":
        print("script for delete operations yet to be written!")

    
    else:
        print("Plese enter a vlid operation(create/delete)")



else:
    print('please enter a valid email address !!')

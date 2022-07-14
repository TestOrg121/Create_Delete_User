#required modules
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
    
    API_KEY= os.environ['CORALOGIX_KEY']
    
    cammand=f"./cxctl account invite --api-key {API_KEY} --region eu --id 35963  --invites {email}:user"
    
    os.system(cammand)

#function for adding user to github
def addUser_github(email):

    ACCESS_TOKEN= os.environ['ACCESS_TOKEN']

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
    
    
#function for adding user to AWS   
def addUser_aws(email):
    
    print("Yet to be written !!")
    
#function for adding user to Appsignal  
def addUser_appsignal(email):
    
    print("Yet to be written !!")
    
#function for adding user to Redash     
def addUser_redash(email):
    
    print("Yet to be written !!")
    
#function for adding user to JIRA     
def addUser_jira(email):
    
    print("Yet to be written !!")
    
#function for adding user to  Jenkins    
def addUser_jenkins(email):
    
    print("Yet to be written !!")

#function for adding user to all platform
def addUser_all(email):
    
    addUser_coralogix(email)
    addUser_github(email)
    addUser_aws(email)
    addUser_appsignal(email)
    addUser_redash(email)
    addUser_jira(email)
    addUser_jenkins(email)

    
#email adsress of user
email = os.environ['email']

#operation to be performed 
operation = os.environ['operation']

#platform on which operation is to be performed 
platform = os.environ['platform']



if email_is_valid(email):

    if operation=="create":

        if platform=="coralogix":

            addUser_coralogix(email)

        elif platform=="github":

            addUser_github(email)

        elif platform=="aws":

            addUser_aws(email)

        elif platform=="appsignal":

            addUser_appsignal(email)

        elif platform=="redash":

            addUser_redash(email)

        elif platform=="jira":

            addUser_jira(email)

        elif platform=="jenkins":

            addUser_jenkins(email)
            
        elif platform=="All":
            
            addUser_all(email)
            
            
    elif operation=="delete":

        print("script for delete operations is yet to be written!")

else:

    print('please enter a valid email address !!')

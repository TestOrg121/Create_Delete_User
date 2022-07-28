#required modules
import re
import os
import requests
import json
import boto3
import pandas
import redashAPI
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

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
    
    print("Script for AWS is yet to be written !!")
    
#function for adding user to Appsignal  
def addUser_appsignal(email):
    
    print("Script for Appsignal is yet to be written !!")
    
#function for adding user to Redash     
def addUser_redash(email):
    
    domain_name=os.environ['DOMAIN_NAME_REDASH']

    API_KEY=os.environ['API_KEY_REDASH']

    Redash=redashAPI.RedashAPIClient(API_KEY,domain_name)

    body={
        "name":email.split('.')[0],
        "email":email,
    }
    
    r=Redash.post("users",body)

    invite_link=r.json()["invite_link"]

    # -- code for sending invitation link to user's email-id --
    
    sender_email=os.environ['SENDGRID_SENDER_EMAIL']
    sg = sendgrid.SendGridAPIClient(api_key=os.environ['SENDGRID_API_KEY'])
    from_email = Email(sender_email)  # Change to your verified sender
    to_email = To(email)  # Change to your recipient
    subject = "Invitivation link for Redash"
    message=f""" 
    Welcome to Redash!
    please click on the link below to setup your password and create your account
    {invite_link}
    """
    content = Content("text/plain",message)
    
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)
    
#function for adding user to JIRA     
def addUser_jira(email):
    
    API_TOKEN= os.environ['API_KEY_JIRA']
    my_email= os.environ['EMAIL_ADMIN_JIRA']
    domain_name= os.environ['DOMAIN_NAME_JIRA']
    
    url = f"https://{domain_name}.atlassian.net/rest/api/2/user"


    auth =(my_email,API_TOKEN)

    headers = {
       "Accept": "application/json",
       "Content-Type": "application/json"
    }

    body = json.dumps( {
      "emailAddress": email
    } )

    response = requests.post(
       url=url,
       data=body,
       headers=headers,
       auth=auth
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    
#function for adding user to  Jenkins    
def addUser_jenkins(email):
    print("Script for Jenkins is yet to be written !!")

#function for adding a user to all platform
def addUser_all(email):
    addUser_coralogix(email)
    addUser_github(email)
    addUser_aws(email)
    addUser_appsignal(email)
    addUser_redash(email)
    addUser_jira(email)
    addUser_jenkins(email)
    
#function to delete a user from jira   
def deleteUser_jira(email):
    domain_name= os.environ['DOMAIN_NAME_JIRA']
    API_TOKEN= os.environ['API_KEY_JIRA']
    my_email= os.environ['EMAIL_ADMIN_JIRA']

    auth =(my_email,API_TOKEN)

    headers = {
       "Accept": "application/json",
       "Content-Type": "application/json"
    }
    
    search_url = f"https://{domain_name}.atlassian.net/rest/api/2/user/search?query={email}"

    response = requests.get(
       url=search_url,
       headers=headers,
       auth=auth
    )

    accountId=response.json()[0]["accountId"]

    delete_url= f"https://{domain_name}.atlassian.net/rest/api/3/user/"
    
    params={
        "accountId":accountId
    }

    r=requests.delete(url=delete_url,params=params,auth=auth)

    print(r.status_code)

#function to delete a user from redash
def deleteUser_redash(email):
    domain_name=os.environ['DOMAIN_NAME_REDASH']

    API_KEY=os.environ['API_KEY_REDASH']

    Redash=redashAPI.RedashAPIClient(API_KEY,domain_name)

    search_uri=f"users?q={email}"

    search_result=Redash.get(search_uri)
    user_id=search_result.json()["results"][0]["id"]

    delete_uri=f"users/{user_id}"

    response=Redash.delete(delete_uri)

    print(response.json())    
    
    
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
        
        if platform=="jira":
            deleteUser_jira(email)
            
        elif platform=="redash":
            deleteUser_redash(email)
            
        else:
            print("script for delete operations is yet to be written!")

else:

    print('please enter a valid email address !!')

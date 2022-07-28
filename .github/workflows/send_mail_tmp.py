import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

SENDER_EMAIL="bibhuti.singh@byjus.com"
email="rahul.a9@byjus.com"
sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
from_email = Email(SENDER_EMAIL)  # Change to your verified sender
to_email = To(email)  # Change to your recipient
subject = "Sending with SendGrid is Fun"

message=f"""
hello friend!
this is your email
{email}
"""
content = Content("text/plain",message)
mail = Mail(from_email, to_email, subject, content)

# Get a JSON-ready representation of the Mail object
mail_json = mail.get()

# Send an HTTP POST request to /mail/send
response = sg.client.mail.send.post(request_body=mail_json)
print(response.status_code)
print(response.headers)

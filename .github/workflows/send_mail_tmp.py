import boto3 
import pandas

# Creating the low level functional client
client = boto3.client(
    's3',
    aws_access_key_id = 'ASIAQ2WETJKF6GU3F4FE',
    aws_secret_access_key = 'foHLt3PZIdUpcSO9g97np9W8/zXZO6OLBhagml+4',
    region_name = 'ap-southeast-1'
)
    

# Create the S3 object
obj = client.get_object(
    Bucket = 'email-username-mapping',
    Key = 'email-username-mapping.csv'
)
    
# Read data from the S3 object
data = pandas.read_csv(obj['Body'])
  
print('Printing the data frame...')
print(data.values)

email="rahul.a9@byjus.com"
#for getting user
df2=data.query(f"email=='{email}'")['username']
print(df2.iat[0])

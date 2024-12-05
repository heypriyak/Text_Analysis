import boto3
from urllib.parse import urlparse

# Function to extract bucket and key from S3 URL
def parse_s3_url(s3_url):
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc.split('.')[0]  # Extract the bucket name
    file_key = parsed_url.path.lstrip('/')  # Extract the file key
    return bucket_name, file_key

# Example S3 link
s3_url = 'https://s3.amazonaws.com/your-bucket-name/your-file-name.txt'

# Extract bucket name and file key
bucket_name, file_key = parse_s3_url(s3_url)

# Use boto3 to read the file
s3 = boto3.client('s3')
response = s3.get_object(Bucket=bucket_name, Key=file_key)

# Read file content
file_content = response['Body'].read().decode('utf-8')
print(file_content)

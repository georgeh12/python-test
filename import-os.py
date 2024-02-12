import os
import boto3

# Explicitly specifying where the default AWS region is found 
# (as an environment variable) to be able to mock it in the test
s3_client = boto3.client('s3', region_name=os.environ['AWS_REGION'])
translate_client = boto3.client('translate', region_name=os.environ['AWS_REGION'])

def lambda_handler(event, context):
    print(event)

    # Get S3 bucket and key name from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key_name = event['Records'][0]['s3']['object']['key']
    print(bucket_name, key_name)

    # If valid .txt file, read S3 file and translate text
    if key_name.endswith('.txt'):
        try:
            bucket_file_contents = read_file(bucket_name, key_name)
        except Exception as e:
            print(e)
            return {
                "success": False,
                "response": f"Failed to read file - {e}"
            }
        try: 
            script_text = configure_script(bucket_file_contents)
        except Exception as e:
            print(e)
            return {
                "success": False,
                "response": f"Failed to configure script - {e}"
            }
    else:
        return {
            "success": False,
            "response": "Invalid file type. File must have .txt extension."
        }

    print(script_text)
    return script_text

def read_file(bucket_name, key_name):

    s3_file = s3_client.get_object(Bucket=bucket_name, Key=key_name)
    s3_file_content = s3_file['Body'].read().decode('utf-8')

    return s3_file_content

def get_aws_parameter(parameter_name):
    # Retrieve the value of an AWS parameter from AWS Systems Manager Parameter Store.
    ssm = boto3.client('ssm', region_name=os.environ['AWS_REGION'])
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response['Parameter']['Value']

def configure_script(script_file_contents):

    # Adding shebang to file
    parsed_response = "#!/usr/bin/env bash\n" + script_file_contents

    aws_parameters = ['user', 'pass']
    # Import environment variables from AWS and add to bash file
    # Be sure that the script runs after the parameters are added
    #TODO: code goes here

    return parsed_response
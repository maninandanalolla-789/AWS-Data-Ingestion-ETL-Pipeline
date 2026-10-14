import json
import boto3
import ast
def lambda_handler(event, context):
    #event={'Records': [{'messageId': 'f92637b9-e99b-41a1-bf21-17acf0525ef7', 'receiptHandle': 'AQEBskzRS7izJ8zqQKpsHhoau1qERBGuvLv7T/iumeJAEj3R0Bmsocu7fjm8Jr2qRm9rZDUymKR8DPskBnlzTjN5vfChsRGsHD4GfwEiBngqAphoShk7TuyE6QsO4jn2BcVDv8FVyoPW7WU+JHA3oVVU0DCcyg2vTMoBJurPIQ/fk0k72MosC/5aFwe34OuGO31BMhHXm0JjPuRUiJ1uD/EM5PFJf1m8VGQDkbvm9yt+QtYVl/iILvMWyP9YnFkCy5f2NAtqJjMAba0SzwyUcMkNO/YBro9q32kjjf1dd0XElPyg0Te2kZqFkgN5uZx+g/h4k/nZr4iHR35xDLzYvN9Llr/BggPjwoM0PXDbN5kQwI5YL5M5opGxa6fovR2ooNl/ZBbrLjtnWBl7jUKCS5Amfw==', 'body': '"{\\"bucket_name\\": \\"projectinjection-246830848764-ap-southeast-2-an\\", \\"file_name\\": \\"source_folder/ingestion_products.csv\\"}"', 'attributes': {'ApproximateReceiveCount': '1', 'AWSTraceHeader': 'Root=1-6a4f8848-6f44c9b3423afd37da21d1b2;Parent=03f472098844b56e;Sampled=0;Lineage=2:2a0138a8:0', 'SentTimestamp': '1783597129016', 'SenderId': 'AROATS6CD3L6PSYUDRI6S:injection_processing', 'ApproximateFirstReceiveTimestamp': '1783597129018'}, 'messageAttributes': {}, 'md5OfBody': '0f41a382babf295b8c9d0d5848db9172', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:ap-southeast-2:246830848764:processedQueue', 'awsRegion': 'ap-southeast-2'}]}
    print(event)
    body = event['Records'][0]['body']
    print('body: ' ,body)
    clean_string = ast.literal_eval(body)
    print(clean_string)

    # # Step 2: Parse the actual JSON payload

    data_dict = json.loads(clean_string)
    print(data_dict)
    print(type(data_dict))
    data_dict['status']='successfull'
    print(data_dict)

    bucket_name = data_dict['bucket_name']
    file_path = data_dict['file_path']
    filename = file_path.split('/')[-1]
    # print('bucket_name: ', bucket_name)
    # print('file_name: ', file_path)

    sns_client = boto3.client('sns')
    sns_client.publish(TopicArn='arn:aws:sns:ap-southeast-2:246830848764:emailcommuication',
    Message=str(data_dict),
    Subject='file process successfully')

    s3_client = boto3.client('s3')

    archivefile='archive_folder/'+ filename
    s3_client.copy_object(
        Bucket=bucket_name,
        CopySource={'Bucket': bucket_name, 'Key': file_path},
        Key= archivefile
        )
    s3_client.delete_object(
        Bucket=bucket_name,
        Key=file_path
    )
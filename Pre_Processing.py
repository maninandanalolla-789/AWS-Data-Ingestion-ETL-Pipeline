import json
import boto3
def lambda_handler(event, context):
    #event={'Records': [{'eventVersion': '2.5', 'eventSource': 'aws:s3', 'awsRegion': 'ap-southeast-2', 'eventTime': '2026-07-30T11:12:09.005Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AFMB9Y97RCD42'}, 'requestParameters': {'sourceIPAddress': '49.204.236.35'}, 'responseElements': {'x-amz-request-id': '15CAFJ4E70ENRC1T', 'x-amz-id-2': 'E/WUWbII+mTptdIknIUwVvkp/alCTBDhR/eNjA3uyTJNAcAmJMOCW5CWUr27UHZAjP63O+xwjMM6CH6Vk8KYeUJ+vaTJmqFN'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'f15d2dfc-d70e-4940-9d72-eadb21f58ad6', 'bucket': {'name': 'projectinjection-246830848764-ap-southeast-2-an', 'ownerIdentity': {'principalId': 'AFMB9Y97RCD42'}, 'arn': 'arn:aws:s3:::projectinjection-246830848764-ap-southeast-2-an'}, 'object': {'key': 'source_folder/ingestion_products.csv', 'size': 15680, 'eTag': '6bedae1580567500f9b2a762630dd89b', 'sequencer': '006A6B3188F3901D0B'}}}]}
    print(event)
    bucket_name = event['Records'][0]['s3']['bucket']['name'] #'dataingestion-842746302582-eu-north-1-an'
    file_path = event['Records'][0]['s3']['object']['key'] #'source/Gana.pdf'
    try:
        data={'bucket_name': bucket_name,'file_path': file_path}
        filepath = data['file_path']          #'source/Gana.pdf'
        filename = filepath.split('/')[-1]      # scenario 1 : 'Gana.pdf'  scenario 2 : 'ingestion_Gana.pdf' scenario 3 : 'ingestion_Gana.txt/csv'
        if filename.startswith('tcs_') or filename.startswith('ingestion_'):
            if filename.endswith('.txt') or filename.endswith('.csv'):
                    sqs_client = boto3.client('sqs')
                    sqs_client.send_message(
                        QueueUrl='https://sqs.ap-southeast-2.amazonaws.com/246830848764/preprcoessingQueue',
                        MessageBody=json.dumps(data)
                    )
            else:
                raise Exception(f'invalid file format {filename}')  #scenario 2 : 'ingestion_Gana.pdf'
        else:
            raise Exception(f'invalid file name {filename}') # scenario 1 : 'Gana.pdf'
    except Exception as e:
        print(str(e))
        s3_client = boto3.client('s3')
        errorfile='failure_folder/'+ filename
        s3_client.copy_object(
            Bucket=bucket_name,
            CopySource={'Bucket': bucket_name, 'Key': file_path},
            Key= errorfile
            )
        s3_client.delete_object(
            Bucket=bucket_name,
            Key=file_path
        )


        raise e
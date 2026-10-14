import json
import boto3
import pandas as pd
import ast
import io
from sqlalchemy import create_engine
import psycopg2


def lambda_handler(event, context):
    # event={'Records': [{'messageId': '6eb8b79d-e256-43bb-a3b4-4baea4241c5f', 'receiptHandle': 'AQEBkfZaK3b4+NmUoLxcg/p/e/YamJuplDXV2tccF4d9NxQI3asJCm4iBNyL3waNfuz4fD7VonkXxbWbVPg0tX+nlxUkkiss86SQ41Svs5u++xzToSurHjfA8KoGkQL+znmOudTLLif0PRrg6XILWJhiqf7NpR2aTjukcFRTVAaG2VR9KI/eKwjzcDMiMain3MRn++KUNyJ5fu23LLscyf+PEWbolEk56dBNQKfZ4/+KqKn37rnR2kW6f5lRSTrWaM8pGorlDlLhoY0IkVWYE/kNAUZFGre1gqOx8yEIpOXkTAk/7LS7Y+pxvZRtkXzqesWGCAhybFjJDM88uZ8Kf7kRAXTkhX8jyPTTlreIJsIwNE4N4XaeVZnuvZUFnvuWTpst+JwDBKzoBOJ95A9hvjo1Ng==', 'body': '{"bucket_name": "projectinjection-246830848764-ap-southeast-2-an", "file_path": "source_folder/ingestion_products.csv"}', 'attributes': {'ApproximateReceiveCount': '21', 'AWSTraceHeader': 'Root=1-6a5ca9bf-0dcf522a0227750014d7f920;Parent=45c57844dcdd8b92;Sampled=0;Lineage=1:4ba55fa0:0', 'SentTimestamp': '1784457665577', 'SenderId': 'AROATS6CD3L6PSYUDRI6S:injection_preprocessing', 'ApproximateFirstReceiveTimestamp': '1784457665589'}, 'messageAttributes': {}, 'md5OfBody': 'f4a7ed9ede0ba8faa3d21ec1589b5592', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:ap-southeast-2:246830848764:preprcoessingQueue', 'awsRegion': 'ap-southeast-2'}]}
    print(event)

    data = event['Records'][0]['body']
    print('body: ', data)
    # cleaning = ast.literal_eval(body)
    # print('cleaning: ', cleaning)
    data2 = json.loads(data)
    print('data2: ', data2)
    bucket_name = data2['bucket_name']
    file_path = data2['file_path']

    s3_client = boto3.client('s3')
    responce = s3_client.get_object(Bucket=bucket_name, Key=file_path)
    print('responce: ', responce)
    print('responce body: ', responce['Body'])

    file = io.BytesIO(responce['Body'].read())
    df = pd.read_csv(file)
    print(df)
    """
    business logic

    """
    # final_Df=df
    rds_client = boto3.client('rds', region_name='ap-southeast-2')

    DB_HOST = "datalineage-database.cr0wky0wgx1w.ap-southeast-2.rds.amazonaws.com"
    DB_PORT = 5432
    DB_USER = "admin2005"
    DB_NAME = "postgres"
    pwd = 'admin123456'

    engine = create_engine(f'postgresql://{DB_USER}:{pwd}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    df.to_sql('products_table', engine, if_exists='replace', index=False)

    sqs_client = boto3.client('sqs')
    sqs_client.send_message(
        QueueUrl="https://sqs.ap-southeast-2.amazonaws.com/246830848764/processedQueue",
        MessageBody=json.dumps(data)
    )
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
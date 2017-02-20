import boto3
import json
import gzip
from elasticsearch import Elasticsearch

def lambda_handler(event, context):
    """ S3 to Elasticsearch """
    s3_client = boto3.client('s3')
    es = Elasticsearch([{'host': '10.0.1.70', 'port': 9200}])
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    s3_client.download_file(bucket, key, '/tmp/' + key)
    data = gzip.open('/tmp/' + event['Records'][0]['s3']['object']['key'], 'rb')
    j = json.load(data)
    if 'Records' in j:
        records = j['Records']
        for item in records:
            cloudtrail_event = "{"
            newline = 0
            for field in item:
                if newline > 0:
                    cloudtrail_event = cloudtrail_event + ","
                newline = 1
                cloudtrail_event = cloudtrail_event + "\"%s\":\"%s\"" % (field, item[field])
            cloudtrail_event = cloudtrail_event + "}"
            es.index(index="cloudtrail",doc_type='cloudtrail_event', body=json.loads(cloudtrail_event))

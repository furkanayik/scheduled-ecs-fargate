import boto3
import json
import logging
from datetime import datetime

from data import Params
import dto


logger = logging.getLogger()

class SnsTopic():
    topic = None

    def __init__(self):
        sns = boto3.resource("sns")
        self.topic = sns.create_topic(Name='mailchimp-import-alerts')

    def publish(self, error='test'):
        message = "Mailchimp import has failed. Error: {}".format(error)
        response = self.topic.publish(
            Subject='Mailchimp-Import-Alert', Message=message)
        message_id = response['MessageId']
        return message_id


def get_s3_list_id():
    s3 = boto3.client('s3')
    s3_clientobj = s3.get_object(
        Bucket=Params.S3_BUCKET_NAME, Key='data.json')
    s3_clientdata = s3_clientobj['Body'].read().decode('utf-8')
    return json.loads(s3_clientdata)['listId']


def get_list_import_history_record(list_id):
    client = boto3.client('dynamodb')
    key = {
        'ListId': {
            'S': list_id
        },
    }
    response = client.get_item(TableName=Params.DYNAMODB_TABLE_NAME,
                               Key=key)

    record = {}
    if ("Item" in response):
        record = dto.deserialize_dynamodb_items(response['Item'])

    return record


def upsert_list_import_history(list_id):
    current_date = datetime.now()
    formated_datetime = current_date.astimezone().replace(microsecond=0).isoformat()

    client = boto3.client('dynamodb')
    key = {
        'ListId': {
            'S': list_id
        }
    }
    update_expression = 'SET LastImportTime = :last_import_time'
    expression_attribute_values = {
        ':last_import_time': {
            'S': formated_datetime
        }
    }

    response = client.update_item(TableName=Params.DYNAMODB_TABLE_NAME,
                                  Key=key,
                                  UpdateExpression=update_expression,
                                  ExpressionAttributeValues=expression_attribute_values,
                                  ReturnValues='ALL_NEW'
                                  )

    logger.info('Upserted dynamodb record: {}'.format(
        dto.deserialize_dynamodb_items(response['Attributes'])))


def put_failed_import_item(list_id, offset):
    current_date = datetime.now()
    formated_datetime = current_date.astimezone().replace(microsecond=0).isoformat()

    client = boto3.client('dynamodb')

    client.put_item(TableName=Params.DYNAMODB__FAILED_IMPORT_TABLE_NAME,
                               Item={
                                   "ListId": {"S": list_id},
                                   "offset": {"N": str(offset)},
                                   "import_try_time": {"S": formated_datetime}
                               })

    logger.info('Failed import details inserted to dynamodb; list_id: {}, offset: {}'.format(
        dto.deserialize_dynamodb_items(list_id, offset)))

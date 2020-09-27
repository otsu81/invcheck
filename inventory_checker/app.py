import json
import logging
import os
import requests
import boto3
from datetime import datetime
from code.boto_factory import BotoFactory

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('inventory_checker')


def __get_dummy_json():
    with open('dummy_json/diff.json', 'r') as f:
        response = json.loads(f.read())
    return response


def lambda_handler(event, context):
    response = requests.get(os.environ.get('URL'))
    # response = __get_dummy_json()

    inventory = response.json()\
        .get('products')\
        .get('product')[0]\
        .get('inventoryStatus')\
        .get('status')

    if not inventory:
        log.warning('API field empty')
    elif inventory != 'PRODUCT_INVENTORY_OUT_OF_STOCK':
        log.warning('ACHTUNG OBER ALLES')

        sns = BotoFactory().get_capability(
            boto3.client, boto3.Session(), 'sns',
            account_id=os.environ.get('ACCOUNT_ID'),
            rolename=os.environ.get('ROLE'),
            region='eu-west-1'
        )

        result = sns.publish(
            TopicArn=os.environ.get('TOPIC_ARN'),
            Subject='ACHTUNG KAUFEN',
            Message=f"API change {inventory}"
        )

        log.info(result)
    else:
        log.info(f"{datetime.now()}: {inventory}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": inventory,
        }),
    }

from __future__ import print_function
import boto3
import json
import os
import traceback
import re

#-----Dynamo Info change here------
TABLE_NAME = os.environ.get('TABLE_NAME', "default")
DDB_PRIMARY_KEY = "device_id"
DDB_SORT_KEY = "time"
TOPIC_PREFIX = "kagawa/kosen/denkilab/rpi/"
#-----Dynamo Info change here------

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def create_item(event):
    pattern = f'^{TOPIC_PREFIX}(\d+)$'
    try:
        topic = event['topic']
        device_id = re.match(pattern, topic).group(1)
        item = {
            DDB_PRIMARY_KEY: int(device_id),
            DDB_SORT_KEY: event['time'],
            "humidity": event['humidity'],
            "temperature": event['temperature'],
            "co2": event['co2']
        }
        print("item:{}".format(item))
        return item

    except Exception as e:
        print(traceback.format_exc())
        return None

#------------------------------------------------------------------------
# call by Lambda here.
#------------------------------------------------------------------------
def lambda_handler(event, context):
    print("lambda_handler start")

    try:
        print("---------------json inside----------------")
        print(json.dumps(event))
        item = create_item(event)
        
        table.put_item(Item=item)
        return
    except Exception as e:
        print(traceback.format_exc())
        raise e

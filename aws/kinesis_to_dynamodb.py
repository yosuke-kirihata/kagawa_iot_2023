from __future__ import print_function
import base64
import boto3
import json
import os
import traceback
from decimal import Decimal
import re

#-----Dynamo Info change here------
TABLE_NAME = os.environ.get('TABLE_NAME', "default")
DDB_PRIMARY_KEY = "device_id"
DDB_SORT_KEY = "time"
TOPIC_PREFIX="kagawa/kosen/denkilab/rpi/"
#-----Dynamo Info change here------

dynamodb = boto3.resource('dynamodb')
table  = dynamodb.Table(TABLE_NAME)

def create_item(payload, device_id):
    try:
        #String to Json object
        payload_data = json.loads(payload, parse_float=Decimal)
        # adjust your data format
        res_dict = {
            DDB_PRIMARY_KEY: int(device_id),
            DDB_SORT_KEY: payload_data['time'],
            "humidity": payload_data['humidity'],
            "temperature": payload_data['temperature'],
            "co2": payload_data['co2']
        }
        print("res_dict:{}".format(res_dict))
        return res_dict

    except Exception as e:
        print(traceback.format_exc())
        return None

def write_item_info(data_list):
    item_info_dict_list = []
    try:
        for data in data_list:
            item_dict = create_item(data[0], data[1]) # (payload, deviceId)
            if None != item_dict:
                item_info_dict_list.append(item_dict)
            # if data does not have key info, just pass
            else:
                print("Error data found:{}".format(data))
                pass

    except Exception as e:
        print(traceback.format_exc())
        print("Error on write_item_info")

    return item_info_dict_list

def dynamo_bulk_put(data_list):
    try:
        put_item_dict_list = write_item_info(data_list)
        with table.batch_writer() as batch:
            for put_item_dict in put_item_dict_list:
                batch.put_item(Item = put_item_dict)
        return

    except Exception as e:
        print("Error on dynamo_bulk_put")
        raise e

def decode_kinesis_data(data_list):
    decoded_list = []
    try:
        for data in data_list:
            payload = base64.b64decode(data['kinesis']['data'])
            partition_key = data['kinesis']['partitionKey']
            device_id = get_device_id_from_partition_key(data['kinesis']['partitionKey'])

            print("payload={}".format(payload))
            print("device_id={}".format(device_id))

            decoded_list.append((payload, device_id))

        return decoded_list

    except Exception as e:
        print("Error on decode_kinesis_data")
        raise e

def get_device_id_from_partition_key(partition_key):
    pattern = f'^{TOPIC_PREFIX}(\d+)$'
    try:
        device_id = re.match(pattern, partition_key).group(1)
        return device_id
    except Exception as e:
        print("Error on get_device_id_from_partition_key")
        raise e



#------------------------------------------------------------------------
# call by Lambda here.
#------------------------------------------------------------------------
def lambda_handler(event, context):
    print("lambda_handler start")

    try:
        print("---------------json inside----------------")
        print(json.dumps(event))
        encode_kinesis_list = event['Records']
        print(encode_kinesis_list)
        decoded_kinesis_list = decode_kinesis_data(encode_kinesis_list)
        # Dynamo Put
        if 0 < len(decoded_kinesis_list):
            dynamo_bulk_put(decoded_kinesis_list)
        else:
            print("there is no valid data in Kinesis stream, all data passed")

        return

    except Exception as e:
        print(traceback.format_exc())
        # This is sample source. When error occur this return success and ignore the error.
        raise e

import os
import requests
import json
import boto3
import decimal
from pytz import timezone
from dateutil import parser

def get_temperature():
    url = 'https://api.nature.global/1/devices'
    token = 'Bearer ' + os.environ['token']
    headers = {'Content-type': 'application/json', 'Authorization': token}

    response = requests.get(url, headers=headers)
    result = json.loads(response.text, parse_float=decimal.Decimal)

    dynamoDB = boto3.resource("dynamodb")
    table = dynamoDB.Table(os.environ['table']) # DynamoDBのテーブル名


    utc_string = result[0]['newest_events']['te']['created_at']
    jst_time = parser.parse(utc_string).astimezone(timezone('Asia/Tokyo'))

    table.put_item(
        Item = {
            "type": 'te', # 温度
            "updated_at": str(jst_time),
            "val" : result[0]['newest_events']['te']['val']
      }
    )

    utc_string = result[0]['newest_events']['hu']['created_at']
    jst_time = parser.parse(utc_string).astimezone(timezone('Asia/Tokyo'))

    table.put_item(
        Item = {
            "type": 'hu', # 湿度
            "updated_at": str(jst_time),
            "val" : result[0]['newest_events']['hu']['val']
        }
    )

    utc_string = result[0]['newest_events']['il']['created_at']
    jst_time = parser.parse(utc_string).astimezone(timezone('Asia/Tokyo'))

    table.put_item(
        Item = {
            "type": 'il', # 照度
            "updated_at": str(jst_time),
            "val" : result[0]['newest_events']['il']['val']
        }
    )



def lambda_handler(event, context):
    get_temperature()


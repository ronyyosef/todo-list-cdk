import json
import os
import uuid

import boto3

from .const import TODO_LIST_TABLE_NAME, TODO_LIST_PARTITION_KEY

table_name = os.environ[TODO_LIST_TABLE_NAME]
dynamodb_resource = boto3.resource('dynamodb')
todo_list_table = dynamodb_resource.Table(table_name)


def create_todo(event, context):
    body = json.loads(event['body'])
    content = body['content']
    new_todo = {
        TODO_LIST_PARTITION_KEY: str(uuid.uuid1()),
        'content': content,
        'is_completed': False
    }
    todo_list_table.put_item(Item=new_todo)
    return {
        "statusCode": 201,  # 201 is the status code for created
        "body": json.dumps(new_todo)
    }

import json
import os

import boto3

from .const import TODO_LIST_TABLE_NAME

table_name = os.environ[TODO_LIST_TABLE_NAME]
dynamodb_resource = boto3.resource('dynamodb')
todo_list_table = dynamodb_resource.Table(table_name)


def get_todo(event, context):
    todos = todo_list_table.scan()['Items']
    return {
        "statusCode": 200,  # 200 is the status code for OK
        "body": json.dumps(todos),
    }

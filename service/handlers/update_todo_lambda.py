import json
import os
import time
from datetime import datetime

import boto3

from .const import TODO_LIST_TABLE_NAME, TODO_LIST_PARTITION_KEY

table_name = os.environ[TODO_LIST_TABLE_NAME]
dynamodb_resource = boto3.resource('dynamodb')
todo_list_table = dynamodb_resource.Table(table_name)


def update_todo(event, context):
    task_id = event['pathParameters']['task_id']
    body = json.loads(event['body'])

    update_expression = "set"
    expression_attribute_values = {}
    if 'content' in body:
        update_expression += " content = :c,"
        expression_attribute_values[':c'] = body['content']
    if 'is_completed' in body:
        update_expression += " is_completed = :i"
        expression_attribute_values[':i'] = body['is_completed']

    update_expression = update_expression.rstrip(',')

    updated_task = todo_list_table.update_item(Key={
        TODO_LIST_PARTITION_KEY: task_id
    },
        UpdateExpression=update_expression,
        ConditionExpression=f"attribute_exists({TODO_LIST_PARTITION_KEY})",
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW")['Attributes']
    return {
        "statusCode": 200,
        "body": json.dumps(updated_task),
    }

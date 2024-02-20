import os

import boto3

from .const import TODO_LIST_TABLE_NAME, TODO_LIST_PARTITION_KEY

table_name = os.environ[TODO_LIST_TABLE_NAME]
dynamodb_resource = boto3.resource('dynamodb')
todo_list_table = dynamodb_resource.Table(table_name)


def delete_todo(event, context):
    task_id = event['pathParameters']['task_id']
    todo_list_table.delete_item(Key={
        TODO_LIST_PARTITION_KEY: task_id
    })
    return {
        "statusCode": 204,  # 204 indicates successful deletion
    }

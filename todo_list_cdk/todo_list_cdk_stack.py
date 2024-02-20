from aws_cdk import (
    Stack, aws_dynamodb, RemovalPolicy, aws_lambda, aws_apigateway,
)
from constructs import Construct

TODO_LIST_TABLE_NAME = 'TODO_LIST_TABLE_NAME'


class ToDoListCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define a new DynamoDB table
        todo_list_dynamodb_table = aws_dynamodb.TableV2(
            self, "ToDoList",
            billing=aws_dynamodb.Billing.on_demand(),
            partition_key=aws_dynamodb.Attribute(name="task_id", type=aws_dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY
        )

        # Define AWS Lambda resources for CRUD operations
        create_todo_lambda = aws_lambda.Function(
            self, "createToDoLambdaHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="handlers.create_todo_lambda.create_todo",
            code=aws_lambda.Code.from_asset("service"),
            environment={
                TODO_LIST_TABLE_NAME: todo_list_dynamodb_table.table_name,
            }
        )

        get_todos_lambda = aws_lambda.Function(
            self, "getToDoLambdaHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="handlers.get_todo_lambda.get_todo",
            code=aws_lambda.Code.from_asset("service"),
            environment={
                TODO_LIST_TABLE_NAME: todo_list_dynamodb_table.table_name,
            }
        )

        update_todo_lambda = aws_lambda.Function(
            self, "updateToDoLambdaHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="handlers.update_todo_lambda.update_todo",
            code=aws_lambda.Code.from_asset("service"),
            environment={
                TODO_LIST_TABLE_NAME: todo_list_dynamodb_table.table_name,
            }
        )

        delete_todo = aws_lambda.Function(
            self, "deleteToDoLambdaHandler",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="handlers.delete_todo_lambda.delete_todo",
            code=aws_lambda.Code.from_asset("service"),
            environment={
                TODO_LIST_TABLE_NAME: todo_list_dynamodb_table.table_name,
            }
        )

        # Grant the Lambda functions the permissions they need to interact with the DynamoDB table
        self._grant_lambdas_access(create_todo_lambda=create_todo_lambda, delete_todo=delete_todo,
                                   get_todos_lambda=get_todos_lambda, update_todo_lambda=update_todo_lambda,
                                   table=todo_list_dynamodb_table)

        # Define an API Gateway
        self.configure_api_gateway(create_todo_lambda=create_todo_lambda, delete_todo=delete_todo,
                                   get_todos_lambda=get_todos_lambda,
                                   update_todo_lambda=update_todo_lambda)

    def configure_api_gateway(self, create_todo_lambda, delete_todo, get_todos_lambda,
                              update_todo_lambda):
        api = aws_apigateway.RestApi(
            self, "ToDoApi",
            rest_api_name="Crud ToDoList API",
            description="This service allows for CRUD operations on a ToDoList"
        )
        todos = api.root.add_resource("api").add_resource("todo")
        task_id_resource = todos.add_resource("{task_id}")
        todos.add_method("POST", aws_apigateway.LambdaIntegration(create_todo_lambda))
        todos.add_method("GET", aws_apigateway.LambdaIntegration(get_todos_lambda))
        task_id_resource.add_method("PUT", aws_apigateway.LambdaIntegration(update_todo_lambda))
        task_id_resource.add_method("DELETE", aws_apigateway.LambdaIntegration(delete_todo))

    def _grant_lambdas_access(self, create_todo_lambda, delete_todo, get_todos_lambda, table,
                              update_todo_lambda):
        table.grant_read_data(get_todos_lambda)
        table.grant_read_write_data(create_todo_lambda)
        table.grant_read_write_data(update_todo_lambda)
        table.grant_read_write_data(delete_todo)

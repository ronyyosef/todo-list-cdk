#!/usr/bin/env python3

import aws_cdk as cdk

from todo_list_cdk.todo_list_cdk_stack import ToDoListCdkStack

app = cdk.App()
ToDoListCdkStack(app, "ToDoListCdkStack")

app.synth()

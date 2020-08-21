# -*- coding: utf-8 -*-
"""
Tailor Example 8

This example introduces the following NEW concepts:
    - For DuplicateTask:
        - Use a query expression for the *args* argument

"""

from tailor.api import PythonTask, DuplicateTask, DAGTask, Workflow

### workflow definition ###

t1 = PythonTask(
    action='builtins.print',
    name='task 1',
)

# alt 1: a single query expression, the args expression is evaluated prior to duplication. TODO: When, more specifically?
dup1 = DuplicateTask(task_def=t1, name='duplicate', args='<% $.inputs.values %>')

# alt 2: a list of query expressions, one duplicated task is created per expression in the list. Expressions
# are evaluated in each duplicate
dup2 = DuplicateTask(task_def=t1, name='duplicate',
                     args=['<% $.inputs.values[0] %>', '<% $.inputs.values[1] %>'])

dag = DAGTask(task_defs=[dup1, dup2], name='dag')

### workflow run ###

# project needs to be configured in <userdir>/.tailor/config.yaml
project_name = None  # using default project, override at will

inputs = {
    'values': [['dup1_arg1', 'dup1_arg2'], ['dup2_arg1', 'dup2_arg2']]
}

# create a workflow:
wf = Workflow(project_name=project_name, task_def=dag, name='duplicate workflow',
              inputs=inputs)

# run the workflow
wf_run = wf.run()

# check the status of the workflow run
print(wf_run)

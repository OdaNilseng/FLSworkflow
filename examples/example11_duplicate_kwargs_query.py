# -*- coding: utf-8 -*-
"""
Tailor Example 11

This example introduces the following NEW concepts:
    - For DuplicateTask definitions:
        - Use a query expression for the *kwargs* argument

"""

from tailor.api import PythonTask, DuplicateTask, DAGTask, Workflow

### workflow definition ###

t1 = PythonTask(
    action='builtins.print',
    name='task 1',
    args=['a', 'few', 'arguments'],
    kwargs={'sep': ' -- '}  # kwargs are provided both here and in Duplicate
)

# alt 1: single query expression
dup1 = DuplicateTask(task_def=t1, name='duplicate', kwargs='<% $.inputs.kwargs %>')

# alt 2: list of query expressions, same behaviour
dup2 = DuplicateTask(task_def=t1, name='duplicate',
                     kwargs=['<% $.inputs.kwargs[0] %>', '<% $.inputs.kwargs[1] %>'])

dag = DAGTask(task_defs=[dup1, dup2], name='dag')

### workflow run ###

# project needs to be configured in <userdir>/.tailor/config.yaml
project_name = None  # using default project, override at will

inputs = {
    'kwargs': [
        {'end': '\n\n'},
        {'end': '\n\n\n'}
    ]
}

# create a workflow:
wf = Workflow(project_name=project_name, task_def=dag, name='duplicate workflow',
              inputs=inputs)

# run the workflow
wf_run = wf.run()

# check the status of the workflow run
print(wf_run)

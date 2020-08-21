# -*- coding: utf-8 -*-
"""
Tailor Example 3

This example introduces the following NEW concepts:
    - For task definitions:
        - Using query expressions.
    - Specifying *inputs* when creating a workflow

Query expressions is a means to parameterize the inputs that are specified in
a task definition. The query will be applied later when the workflow is
executed and the parameters to use will be extracted from the input provided
to that specific workflow run. To use a query, the query string must be on the
format "<% query %>". The yaql python package is used for handling queries, see
https://yaql.readthedocs.io/en/latest/index.html.

Inputs are immutable, in the sense that they cannot be changed during the execution
of the workflow.

NOTE: Currently this mechanism only work with data that is directly
JSON-serializable. In the future non-JSON compatible objects will be handled
as well (by use of pickling).
"""
from tailor.api import PythonTask, DAGTask, Workflow

### workflow definition ###

t1 = PythonTask(
    action='time.sleep',
    name='task 1',
    args='<% $.inputs.sleeptime %>'
)
t2 = PythonTask(
    action='builtins.print',
    name='task 2',
    args=['\nSlept for', '<% $.inputs.sleeptime %>', 'second'],
    kwargs={'sep': '   ', 'end': '\n\n'},
    parents=t1
)

dag = DAGTask(task_defs=[t1, t2], name='dag')

### run workflow ###

# project needs to be configured in <userdir>/.tailor/config.yaml
project_name = None  # using default project, override at will

# define inputs
inputs = {
    'sleeptime': 1.5  # try to change this and rerun the workflow
}

# create a workflow:
wf = Workflow(project_name=project_name, task_def=dag, name='inputs workflow',
              inputs=inputs)

# run the workflow
wf_run = wf.run()

# check the status of the workflow run
print(wf_run)

# inputs are available on the run object
print("Inputs are:")
print(wf_run.inputs)

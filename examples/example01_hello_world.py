# -*- coding: utf-8 -*-
"""
Tailor Example 1

This is the Hello world example for tailor.

This example introduces the following NEW concepts:
    - Create PythonTask and DAG definitions
    - For PythonTask definitions:
        - Specifying the action to run (must be an importable python callable)
        - Specifying a name for the task
        - Specifying positional arguments (*args) to the action
        - Specifying relationships between tasks
    - For DAG definitions:
        - Specifying which tasks are part of the DAG
        - Specifying a name for the DAG
    - Create and run a Workflow locally in serial mode
    - Check status of the workflow run
"""

from tailor.api import PythonTask, DAGTask, Project

### workflow definition ###

t1 = PythonTask(
    action='builtins.print',
    name='task 1',
    args='\nHello, world!\n',  # equivalent to ['\nHello, world!\n']
)
t2 = PythonTask(
    action='builtins.print',
    name='task 2',
    args=['\nHello again,', 'world!\n'],
    parents=t1
)

dag = DAGTask(task_defs=[t1, t2], name='dag')

### workflow run ###

# open a project
# (project needs to be configured in <userdir>/.tailor/config.yaml)
project_name = None  # using default project, override at will
prj = Project(project_name)

# create a workflow
wf = prj.new_workflow(
    task_def=dag,
    name='Hello world workflow',
    mode='serial'  # serial (default) or parallel
)

# create a workflow with direct instantiation:
# wf = Workflow(
#     project_name=project_name,
#     task_def=dag,
#     name='Hello world workflow',
#     mode='serial'  # serial (default) or parallel
#     )

# run the workflow
wf_run = wf.run()

# check the status of the workflow run
print(wf_run)

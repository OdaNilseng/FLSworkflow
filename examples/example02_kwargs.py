# -*- coding: utf-8 -*-
"""
Tailor Example 2

This example introduces the following NEW concepts:
    - For PythonTask definitions:
        - Specifying keyword arguments (**kwargs) to the action
"""

from tailor.api import PythonTask, DAGTask, Workflow

### workflow definition ###

t1 = PythonTask(
    action='time.sleep',
    name='task 1',
    args=1
)
t2 = PythonTask(
    action='builtins.print',
    name='task 2',
    args=['\nSlept for', '1', 'second'],
    kwargs={'sep': '   ', 'end': '\n\n'},
    parents=t1
)

dag = DAGTask(task_defs=[t1, t2], name='dag')

### workflow run ###

# project needs to be configured in <userdir>/.tailor/config.yaml
project_name = None  # using default project, override at will

# create a workflow:
wf = Workflow(project_name=project_name, task_def=dag, name='kwarg workflow')

# run the workflow
wf_run = wf.run()

# check the status of the workflow run
print(wf_run)

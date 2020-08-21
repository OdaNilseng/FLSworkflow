# -*- coding: utf-8 -*-
"""
Tailor Example 9

This example introduces the following NEW concepts:
    - For DuplicateTask definitions:
        - Usage of the *kwargs* argument

The principle for duplication using the *kwargs* argument can be illustrated by
the following schematics:

                +---------------------------+
                |         Duplicate         |
                |                           |
                | task=t1                   |
                | kwargs=[{k1:v1}, {k2:v2}] |
                +---------------------------+
                              |
                 +-----------------------+
                 |                       |
        +--------v-------+      +--------v--------+
        | Task (t1)      |      | Task (t1)       |
        | kwargs={k1:v1} |      |  kwargs={k2:v2} |
        +----------------+      +-----------------+

"""

from tailor.api import PythonTask, DuplicateTask, DAGTask, Workflow

### workflow definition ###

# task to duplicate (note that no kwargs are specified)
t1 = PythonTask(
    action='builtins.print',
    name='task 1',
    args=['foo', 'bar']
)
dup = DuplicateTask(task_def=t1, name='duplicate', kwargs=[
    {'sep': ' - ', 'end': '\n\n'},
    {'sep': ' --- ', 'end': '\n\n\n'}
])

dag = DAGTask(task_defs=dup, name='dag')

### workflow run ###

# project needs to be configured in <userdir>/.tailor/config.yaml
project_name = None  # using default project, override at will

# create a workflow:
wf = Workflow(project_name=project_name, task_def=dag, name='duplicate workflow')

# run the workflow
wf_run = wf.run()

# check the status of the workflow run
print(wf_run)

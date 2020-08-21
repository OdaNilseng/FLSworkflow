# -*- coding: utf-8 -*-
"""
Tailor Example 6

This example introduces the following NEW concepts:
    - Use DuplicateTask to duplicate a single PythonTask
    - For Duplicate definitions:
        - Usage of the *args* argument

The principle for duplication using the *args* argument can be illustrated by
the following schematics:

                +-----------+
                | Duplicate |
                |           |
                | task=t1   |
                | args=[1,2]|
                +-----------+
                      |
            +------------------+
            |                  |
      +-----v-----+      +-----v-----+
      | Task (t1) |      | Task (t1) |
      |  args=[1] |      |  args=[2] |
      +-----------+      +-----------+

Duplicated tasks always become children of the Duplicatetask that created them.

"""

from tailor.api import PythonTask, DuplicateTask, DAGTask, Workflow

### workflow definition ###

# task to duplicate (note that no args are specified)
t1 = PythonTask(
    action='builtins.print',
    name='task 1',
)
dup = DuplicateTask(task_def=t1, name='duplicate',
                    args=['Duplicated 1', 'Duplicated 2'])

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

# -*- coding: utf-8 -*-
"""
Tailor Example 7

This example introduces the following NEW concepts:
    - Use the DuplicateTask to duplicate a DAG
    - Specify *args* both in Duplicate and in tasks to be duplicated

When duplicating a Workflow, args are passed to all "root" tasks of that
workflow (i.e. those tasks without parents).

A simple workflow (sub_wf) to be duplicated can be illustrated as:

When *args* are  already specified on task(s) which will receive *args* from
the DuplicateTask, the args already present will be overwritten.

+-----------+       +-----------+
| Task (t1) |       | Task (t2) |
|           |       |           |
+-----+-----+       +-----+-----+
      |                   |
      +---------+---------+
                |
       +--------v--------+
       | Task (t3)       |
       | parents=[t1,t2] |
       +-----------------+

Here t1 and t2 are root tasks and will receive args from the duplicate task as
illustrated here:

                              +------------+
                              | Duplicate  |
                              |            |
                              | task=sub_wf|
                              | args=[1,2] |
                              +-----+------+
                                    |
      +-------------------+---------+--------+-------------------+
      |                   |                  |                   |
      |                   |                  |                   |
+-----v-----+       +-----v-----+      +-----v-----+       +-----v-----+
| Task (t1) |       | Task (t2) |      | Task (t1) |       | Task (t2) |
| args=[1]  |       | args=[1]  |      | args=[2]  |       | args=[2]  |
+-----+-----+       +-----+-----+      +-----+-----+       +-----+-----+
      |                   |                  |                   |
      +---------+---------+                  +---------+---------+
                |                                      |
       +--------v--------+                    +--------v--------+
       | Task (t3)       |                    | Task (t3)       |
       | parents=[t1,t2] |                    | parents=[t1,t2] |
       +-----------------+                    +-----------------+


"""

from tailor.api import PythonTask, DuplicateTask, DAGTask, Workflow

### workflow definition ###


# task to duplicate (note that no args are specified)
t1 = PythonTask(
    action='builtins.print',
    name='task 1',
)
t2 = PythonTask(
    action='builtins.print',
    name='task 2',
    args=['This arg will be overwritten by the DuplicateTask']
)
t3 = PythonTask(
    action='builtins.print',
    name='task 3',
    args='Hello from task 3 which got no args from duplicate...',
    parents=[t1, t2]
)

sub_dag = DAGTask(task_defs=[t1, t2, t3], name='sub-dag')

dup = DuplicateTask(task_def=sub_dag, name='duplicate',
                    args=['Duplicated 1', 'Duplicated 2'])

# outer workflow
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

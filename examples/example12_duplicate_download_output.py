# -*- coding: utf-8 -*-
"""
Tailor Example 12

This example introduces the following NEW concepts:
    - For DuplicateTask definitions:
        - Usage of the *download* argument
    - How links between tasks are treated when Duplicate-tasks are run
    - Behaviour when using the *output* argument in duplicated tasks

In this example the *download* argument to Duplicate is given as a single file
tag. For the duplication to make sense, this file tag should then refer to
several files. Here, three files are uploaded under this file tag which then
creates three duplicates. Only the root-tasks of the duplicated workflow will
get download arguments from the Duplicate-task.

In the example, a sub-workflow (sub_wf) is duplicated for each file stored under
the 'input_files' tag. In addition to the duplicate task (dup) a child task (t3)
is included in the main workflow (wf) to show two concepts:

    1.  How links are treated when a Duplicate task is run. In the initial state
        of wf (the outer workflow), t3 is a child of dup. When the Duplicate
        task is run, the leaf tasks (i.e. those tasks without children) of
        sub_wf becomes parents of t3 as shown in the illustration below. As
        already shown in previous examples, the root tasks of sub_wf become
        children of dup.
    2.  How data available on the workflows' *outputs* are scoped according to
        the duplication level from which it is accessed. In t1, the action is
        glob.glob('*') and the output is put on the 'downloaded_files' output
        name. This output is used in two downstream tasks as arguments to
        builtins.print (with args='<% $.outputs.downloaded_files %>'). In the
        first downstream task t2, which is at the same duplication level as t1,
        only the value from the parent t1 task is accessed. In t3 however,
        which is outside of t1's duplication level, 'downloaded_files'
        needs to be scoped differently. t3 should have access to all values of
        'downloaded_files' which was created in the different duplicated t1 tasks,
        and as can be seen when printed from t3, 'downloaded_files' is now a
        dict with duplicate index as keys and the corresponding 'downloaded_files'
        value as values.


The workflow is illustrated below.

            sub_wf:                     wf before duplication:

      +-----------------+             +------------------------+
      |    Task (t1)    |             |     Duplicate (dup)    |
      |                 |             | task=sub_wf            |
      +--------+--------+             | download='input_files' |
               |                      +-----------+------------+
               |                                  |
               |                                  |
      +--------v--------+                +--------v--------+
      |    Task (t2)    |                |    Task (t3)    |
      | parents=t1      |                | parents=dup     |
      +-----------------+                +-----------------+



                        wf after duplication:

                      +------------------------+
                      |     Duplicate (dup)    |
                      | task=sub_wf            |
                      | download='input_files' |
                      +-----------+------------+
                                  |
                                  |
         +-------------------------------------------------+
         |                        |                        |
+--------v--------+      +--------v--------+      +--------v--------+
|     Task (t1)   |      |     Task (t1)   |      |     Task (t1)   |
|download=        |      |download=        |      |download=        |
|'testfile_01.txt'|      |'testfile_02.txt'|      |'testfile_03.txt'|
+--------+--------+      +--------+--------+      +--------+--------+
         |                        |                        |
         |                        |                        |
         |                        |                        |
+--------v--------+      +--------v--------+      +--------v--------+
|    Task (t2)    |      |    Task (t2)    |      |    Task (t2)    |
| parents=t1      |      | parents=t1      |      | parents=t1      |
+--------+--------+      +--------+--------+      +--------+--------+
         |                        |                        |
         |                        |                        |
         +-------------------------------------------------+
                                  |
                         +--------v--------+
                         |    Task (t3)    |
                         | parents=dup     |
                         +-----------------+

"""
from pprint import pprint

from tailor.api import PythonTask, DuplicateTask, DAGTask, Workflow

### workflow definition ###

# sub-dag to duplicate (note that no download is specified)
t1 = PythonTask(
    action='glob.glob',
    name='task 1',
    args='*',
    output_to='downloaded_files'
)
t2 = PythonTask(
    action='builtins.print',
    name='task 2',
    args='<% $.outputs.downloaded_files %>',
    parents=t1
)
sub_dag = DAGTask(task_defs=[t1, t2], name='sub-dag')

dup = DuplicateTask(task_def=sub_dag, name='duplicate', download='input_files')

t3 = PythonTask(
    action='builtins.print',
    name='task 3',
    args='<% $.outputs.downloaded_files %>',
    parents=dup
)

dag = DAGTask(task_defs=[dup, t3], name='dag')

### workflow run ###

# project needs to be configured in <userdir>/.tailor/config.yaml
project_name = None  # using default project, override at will

files = {
    'input_files':
        ['testfiles/testfile_01.txt',
         'testfiles/testfile_02.txt',
         'testfiles/testfile_03.txt']
}

# create a workflow:
wf = Workflow(project_name=project_name, task_def=dag, name='files workflow',
              files=files)

# run the workflow
wf_run = wf.run()

# check the status of the workflow run
print(wf_run)

print("Outputs are")
pprint(wf_run.outputs)

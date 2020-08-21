# -*- coding: utf-8 -*-
"""
Tailor Example 13

This example shows how to pass downloaded file name(s) as arguments to an action.

"""
from tailor.api import PythonTask, DuplicateTask, DAGTask, Workflow

### workflow definition ###

# sub-dag to duplicate (note that no download is specified)
t1 = PythonTask(
    action='shutil.copyfile',
    name='task 1',
    args=['<% $.storage.inpfile %>'],  # inpfile is a tag
    download='inpfile',
    upload={'outfile': 'newfile*.txt'}
)
t2 = PythonTask(
    action='builtins.print',
    name='task 2',
    args='<% $.storage.outfile %>',
    parents=t1
)
sub_dag = DAGTask(task_defs=[t1, t2], name='sub-dag')

dup = DuplicateTask(task_def=sub_dag, name='duplicate', kwargs='<% $.inputs.outnames %>')

t3 = PythonTask(
    action='builtins.print',
    name='task 3',
    args='<% $.storage.outfile %>',
    parents=dup
)

dag = DAGTask(task_defs=[dup, t3], name='dag')

### workflow run ###

# project needs to be configured in <userdir>/.tailor/config.yaml
project_name = 'Test'  # using default project, override at will

files = {
    'inpfile': 'testfiles/testfile_01.txt'
}

inputs = {
    'outnames': [{'dst': 'newfile_01.txt'}, {'dst': 'newfile_02.txt'}]
}

# create a workflow:
wf = Workflow(project_name=project_name, task_def=dag, name='files workflow',
              inputs=inputs, files=files)

# run the workflow
wf_run = wf.run()

# check the status of the workflow run
print(wf_run)

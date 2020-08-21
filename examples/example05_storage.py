# -*- coding: utf-8 -*-
"""
Tailor Example 5

This example introduces the following NEW concepts:
    - For task definitions:
        - Specifying files to download before running the task
        - Specifying files to upload after task is run
    - Specify which local files to upload when a workflow is created

The *download* argument to Task can be a single file tag (str) or a list of file
tags. These file tags refer to files in the storage location associated with
a workflow-run.

To send input files into a workflow-run the following steps are taken:
    1. Instantiate a storage object
    2. Upload files to the storage object with an associated tag
    3. Pass the storage object along when running the workflow
    4. Tasks will now download files by referencing the file tags.

The *upload* argument to Task is used to specify files to send back to the
storage object after a task has been run. *upload* must be a dict of (tag: val),
where val can be:
    1. one or more query expressions(str and list of str) which is applied
       to action_output. The query result is then searched for actual files,
       these files are then uploaded to storage under the given tag.
    2. one or more glob-style strings (str and list of str) which is applied
       in the task's working dir. Matching files are uploaded under the
       given tag.

File names can also be accessed with queries: "<% $.storage.<tag> %>"
"""

from tailor.api import PythonTask, DAGTask, Workflow

### workflow definition ###

t1 = PythonTask(
    action='glob.glob',
    name='task 1',
    args='*',
    download='testfiles',  # refers to a file tag
    output_to='downloaded_files'
)
t2 = PythonTask(
    action='shutil.copyfile',
    name='task 2',
    args=['<% $.storage.inpfile %>', 'newfile.txt'],  # inpfile is a tag
    download='inpfile',
    upload={'outfile': 'newfile.txt'}
)
t3 = PythonTask(
    action='builtins.print',
    name='task 3',
    args=['Downloaded', '<% $.storage.outfile %>'],
    download='outfile',
    parents=t2
)

dag = DAGTask(task_defs=[t1, t2, t3], name='dag')

### workflow run ###

# project needs to be configured in <userdir>/.tailor/config.yaml
project_name = None  # using default project, override at will

# files to upload is specified in a tag: file(s) dict
files = {
    'testfiles':
        [
            'testfiles/testfile_01.txt',
            'testfiles/testfile_02.txt'
        ],
    'inpfile': 'testfiles/testfile_03.txt'
}

# create a workflow:
wf = Workflow(project_name=project_name, task_def=dag, name='files workflow',
              files=files)

# run the workflow
wf_run = wf.run()

# check the status of the workflow run
print(wf_run)

# print the output of task 1
print('Downloaded files:\n', wf_run.outputs.get('downloaded_files'))

# print content of storage resource
print('Files in workflow storage:\n', wf_run.get_file_list())

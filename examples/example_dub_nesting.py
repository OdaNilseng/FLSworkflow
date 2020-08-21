[13.57]
Bernt
Sørby

from tailor.api import PythonTask, DuplicateTask, DAG, Workflow

t1 = PythonTask(
    name='task 1',
    action='builtins.print'
)
dup1 = DuplicateTask(
    name='dup 1',
    definition=t1
)
dup2 = DuplicateTask(
    name='dup 2',
    definition=dup1
)
dup3 = DuplicateTask(
    name='dup 3',
    definition=dup2,
    args='<% $.inputs.args %>'
)
dag = DAG(
    name='nested dup dag',
    definitions=dup3
)

inputs = {
    'args': [[[[2, 1, 1], [1, 1, 2], [1, 1, 3]],
              [[1, 4, 1], [1, 2, 2], [1, 2, 3]]],
             [[6, 7, 8],
              [9, 10, 11]]]
}

wf = Workflow(
    project_name='Test',
    definition=dag,
    name=dag.name,
    inputs=inputs
)
# run the workflow
wf_run = wf.run()






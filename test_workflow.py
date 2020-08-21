from tailor.api import PythonTask, DAGTask, Workflow
import json

# files = dict(input_file='input_file.json')


"""Load json input files to dict as inputs"""
hull_input = json.load(open('hull.json'))
env_input = json.load(open('environment.json'))
plate_input = json.load(open('plate.json'))

inputs = dict(hull=hull_input, env=env_input, plate=plate_input)

"""Define FLS plate check tasks """
t1 = PythonTask(
    action='fatigue.load_json',
    name='Load input data',
    args=['<% $.storage.input_file %>', ],
    output_to='input_data',
    download='input_file'
)

t2 = PythonTask(
    action='',
    name='From dict to class',
    args=['<% $outputs.input_data %>'],
    parents=[t1]
    # definer output
)



t3 = PythonTask(
    action='fatigue.get_panel_pressure',
    name='Get panel pressure',
    args=['<% $.outputs.input_data %>'],  # input as class
    parents=[t2],
    output_to=''
)

t4 = PythonTask(
    action='fatigue.calc_int_pressure',
    name='Calculate internal pressure',
    # args=['<% $.outputs.input_data %>'], # input as class
    parents=[t2],
    # Send output to pressure = [int, ext]
)

t5 = PythonTask(
    action='fatigue.splash_zone_correction',
    name='Splash zone correction',
    # args=['<% $.outputs.input_data %>'], # input plate loc, lc, wl_pressure
    parents=[t3],
    # output_to=''
)

t6 = PythonTask(
    action='fatigue.calc_stress',
    name='Calculate int and ext stress',
    # args=[pressure]
    parents=[t4, t5],
    output_to=''
)

t7 = PythonTask(
    action='fatigue.calc_stress_fraction',
    name='Calculate stress fraction',
    #args=['<% $.outputs.input_data %>'],  # input as class
    parents=[t6],
    output_to=''
)

t8 = PythonTask(
    action='fatigue.damage',
    name='Calculate fatigue damage',

)

dag = DAGTask(task_defs=[t1, t2, t3], name='dag')

# workflow run #

# open a project
# (project needs to be configured in <userdir>/.tailor/config.yaml)
project_name = None  # using default project, override at will
# prj = Project(project_name)


# create a workflow
# wf = prj.new_workflow(
#     task_def=dag,
#     name='Hello world workflow',
#     mode='serial'  # serial (default) or parallel
# )

wf = Workflow(project_name=project_name, task_def=dag, name='inputs workflow',
              files=files)

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

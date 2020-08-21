from tailor.api import PythonTask, DAGTask, Workflow, DuplicateTask
import json


""" Define data model panel"""
t1 = PythonTask(
    action='fatigue.panel_model',
    name='create panel model',
    args=[],
    output_to=[]
)


""" Calc int and ext stress + splash zone correction--> stress fraction  """
t2 = PythonTask(
    action='fatigue.calc_fls_stress',
    name=''
)


""" Calc damage 
    input: 
    SN-data
    Weibull dist. parameters
    Design life
    Corrosion
"""


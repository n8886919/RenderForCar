import os
import sys
import time
import numpy as np

from global_variables import *
from rendercar_modules.blender_helper import *

ele_amx = 45
model_list = g_syn_model_list
model_list = list(np.loadtxt(model_list, dtype='str'))
model_list_path = os.path.join(g_shapenet_root_folder, '02958343')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(BASE_DIR, 'test/3.jpg')

init_render_engine()
delete_light()
set_background(path=background_path)
pub = init_ros_node()

while not rospy.is_shutdown():
    remove_all_mesh()
    n = np.random.randint(len(model_list))
    n = os.path.join(model_list_path, model_list[n], 'model.obj')
    #n = '/home/showay/Desktop/RenderForCar/datasets/shapenetcore/02958343/1a64bf1e658652ddb11647ffa4306609/model.obj'
    import_obj(n)
    for counter in range(10):
        azi = np.random.rand() * 360
        ele = np.random.rand() * ele_amx
        set_camera_from_angle(azi, ele, 1.5)
        material_randomize()
        render(pub_node=pub)

'''
export PYTHONPATH=$PYTHONPATH:~/Desktop/RenderForCar
blender /home/$USER/Desktop/RenderForCar/blank.blend --python render_ros.py
'''

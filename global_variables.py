#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
#g_ros_path = '/opt/ros/melodic/lib/python2.7/dist-packages'
#g_python_env_path = '/home/nolan/miniconda3/envs/py2/lib/python2.7/site-packages'
g_ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'
g_python_env_path = '/home/showay/anaconda3/envs/py2/lib/python2.7/site-packages'
g_python_env_path2 = '/usr/local/lib/python3.5/dist-packages'

#g_blender_executable_path = '/home/showay/Desktop/RenderForCar/data/blender-2.79b-linux-glibc219-x86_64/blender'
g_blender_executable_path = '/usr/bin/blender'
g_render4cnn_root_folder = os.path.dirname(os.path.abspath(__file__))
g_data_folder = os.path.abspath(os.path.join(g_render4cnn_root_folder, 'data'))
g_datasets_folder = os.path.abspath(os.path.join(g_render4cnn_root_folder, 'datasets'))

g_shapenet_root_folder = os.path.join(g_datasets_folder, 'shapenetcore')
g_sun2012_image_folder = os.path.join(g_datasets_folder, 'sun2012pascalformat/JPEGImages')
g_syn_model_list = os.path.abspath(
    os.path.join(g_render4cnn_root_folder, 'rendercar_modules/selected_704models.txt'))

g_syn_images_folder = '/media/showay/newDisk/nolan/color_material_elemax30'

g_syn_images_num_per_CAD = 100
g_syn_rendering_thread_num = 3


# ------------------------------------------------------------
# RENDER FOR CNN PIPELINE
# ------------------------------------------------------------
g_shape_synset_name_pairs = [('02691156', 'aeroplane'),
                             ('02834778', 'bicycle'),
                             ('02858304', 'boat'),
                             ('02876657', 'bottle'),
                             ('02924116', 'bus'),
                             ('02958343', 'car'),
                             ('03001627', 'chair'),
                             ('04379243', 'diningtable'),
                             ('03790512', 'motorbike'),
                             ('04256520', 'sofa'),
                             ('04468005', 'train'),
                             ('03211117', 'tvmonitor')]
g_shape_synsets = [x[0] for x in g_shape_synset_name_pairs]
g_shape_names = [x[1] for x in g_shape_synset_name_pairs]

g_blank_blend_file_path = os.path.join(g_render4cnn_root_folder, 'blank.blend')
g_view_distribution_folder = os.path.join(g_data_folder, 'view_distribution')
g_view_distribution_files = dict(zip(g_shape_synsets, [os.path.join(g_view_distribution_folder, name+'.txt') for name in g_shape_names]))
# render_model_views
'''
g_syn_light_num_lowbound = 0
g_syn_light_num_highbound = 2
g_syn_light_dist_lowbound = 8
g_syn_light_dist_highbound = 20
g_syn_light_energy_mean = 2
g_syn_light_energy_std = 2
'''

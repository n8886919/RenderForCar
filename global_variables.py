#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import socket

g_render4cnn_root_folder = os.path.dirname(os.path.abspath(__file__))
# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
g_blender_executable_path = '~/Desktop/RenderForCar/blender-2.71-linux-glibc211-x86_64/blender' #!! MODIFY if necessary
g_data_folder = os.path.abspath(os.path.join(g_render4cnn_root_folder, 'data'))
g_datasets_folder = os.path.abspath(os.path.join(g_render4cnn_root_folder, 'datasets'))
g_shapenet_root_folder = os.path.join(g_datasets_folder, 'shapenetcore')
g_sun2012pascalformat_root_folder = os.path.join(g_datasets_folder, 'sun2012pascalformat')


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

g_syn_images_folder = os.path.join(g_data_folder, 'syn_images')
g_syn_images_bkg_overlaid_folder = os.path.join(g_data_folder, 'syn_images_cropped_bkg_overlaid')
#g_syn_bkg_folder = os.path.join(g_sun2012pascalformat_root_folder, 'JPEGImages')
g_blank_blend_file_path = os.path.join(g_render4cnn_root_folder, 'blank.blend') 
g_syn_images_num_per_CAD = 100
g_syn_rendering_thread_num = 5

g_view_distribution_folder = os.path.join(g_data_folder, 'view_distribution')
g_view_distribution_files = dict(zip(g_shape_synsets, [os.path.join(g_view_distribution_folder, name+'.txt') for name in g_shape_names]))
# render_model_views
g_syn_light_num_lowbound = 0
g_syn_light_num_highbound = 6
g_syn_light_dist_lowbound = 8
g_syn_light_dist_highbound = 20
g_syn_light_azimuth_degree_lowbound = 0
g_syn_light_azimuth_degree_highbound = 360
g_syn_light_elevation_degree_lowbound = -90
g_syn_light_elevation_degree_highbound = 90
g_syn_light_energy_mean = 2
g_syn_light_energy_std = 2
g_syn_light_environment_energy_lowbound = 0
g_syn_light_environment_energy_highbound = 1

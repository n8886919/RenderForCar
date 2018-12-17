#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
RENDER_MODEL_VIEWS.py
brief:
    render projections of a 3D model from viewpoints specified by an input parameter file
usage:
    blender blank.blend --background --python render_model_views.py
    -- <shape_obj_filename> <shape_category_synset> <shape_model_md5> <shape_view_param_file> <syn_img_output_folder>

inputs:
       <shape_obj_filename>: .obj file of the 3D shape model
       <shape_category_synset>: synset string like '03001627' (chairs)
       <shape_model_md5>: md5 (as an ID) of the 3D shape model
       <shape_view_params_file>: txt file - each line is '<azimith angle> <elevation angle> <in-plane rotation angle> <distance>'
       <syn_img_output_folder>: output folder path for rendered images of this model

author: hao su, charles r. qi, yangyan li
'''

import os
import bpy
import sys

import random
import numpy as np

# Load rendering light parameters
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(BASE_DIR + '/module')
from global_variables import *
from rendercar_modules.blender_helper import *
'''
light_num_lowbound = g_syn_light_num_lowbound
light_num_highbound = g_syn_light_num_highbound
light_dist_lowbound = g_syn_light_dist_lowbound
light_dist_highbound = g_syn_light_dist_highbound
'''
bg_images = os.listdir(g_sun2012_image_folder)
# Input parameters

shape_file = sys.argv[-5]
shape_synset = sys.argv[-4]
shape_md5 = sys.argv[-3]
shape_view_params_file = sys.argv[-2]
syn_images_folder = sys.argv[-1]
'''
shape_file = '/home/nolan/Desktop/RenderForCar/datasets/shapenetcore/02958343/1a0c91c02ef35fbe68f60a737d94994a/model.obj'
shape_synset = '02958343'
shape_md5 = '1a0c91c02ef35fbe68f60a737d94994a'
shape_view_params_file = '/home/nolan/Desktop/RenderForCar/data/tmp_view_AfWStL/tmpWY5faY'
syn_images_folder = '/home/nolan/Desktop/RenderForCar/data/syn_images/02958343/1a0c91c02ef35fbe68f60a737d94994a'
'''
if not os.path.exists(syn_images_folder):
    os.mkdir(syn_images_folder)

view_params = [[float(x) for x in line.strip().split(' ')] for line in open(shape_view_params_file).readlines()]

init_render_engine(film_transparent=True)
import_obj(mdl=shape_file)

for img_num, param in enumerate(view_params):
    azi = param[0]
    ele = param[1]
    theta = param[2]
    rho = param[3]
    #label = param[4]
    denoising_strength = np.random.rand()
    samples = 2 ** np.random.randint(4, high=9)
    set_render_engine(denoising_strength=denoising_strength, samples=samples)

    delete_light()

    # set point lights
    '''
    for i in range(random.randint(light_num_lowbound, light_num_highbound)):
        light_azimuth_deg = np.random.uniform(0, 360)
        light_elevation_deg = np.random.uniform(0, 90)
        light_dist = np.random.uniform(light_dist_lowbound, light_dist_highbound)
        lx, ly, lz = obj_centened_camera_pos(light_dist, light_azimuth_deg, light_elevation_deg)
        set_light(xyz=(lx, ly, lz))
        # random strength, rgba
    '''
    set_camera_from_angle(azi, ele, rho)
    img_index = np.random.randint(len(bg_images))
    bg_image = os.path.join(g_sun2012_image_folder, bg_images[img_index])
    set_background(bg_image)

    if img_num%5 == 4:
        material_randomize()

    syn_image_file = './no%d_azi%d_ele%d.png' % (img_num, azi*100, ele*100)
    path = os.path.join(syn_images_folder, syn_image_file)
    render(path=path)

    img_num += 1

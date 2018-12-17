#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import os
import sys
import shutil
import random
import tempfile
import datetime
from functools import partial
from multiprocessing.dummy import Pool
from subprocess import call

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

model_list = g_syn_model_list

def load_one_category_shape_list(shape_synset):
    '''
    @input:
        shape_synset e.g. '03001627' (each category has a synset)
    @output:
        a list of (synset, md5, obj_filename, g_syn_images_num_per_CAD) for each shape of that synset category
        where synset is the input synset, md5 is md5 of one shape in the synset category,
        obj_filename is the obj file of the shape, g_syn_images_num_per_CAD is the number of images to render for that shape
    '''
    # return a list of (synset, md5, numofviews) tuples
    shape_md5_list = os.listdir(os.path.join(g_shapenet_root_folder, shape_synset))

    shape_list = [(
        shape_synset,  # e.g. '02958343'
        shape_md5,   # e.g. 1a0bc9ab92c915167ae33d942430658c
        os.path.join(
            g_shapenet_root_folder,
            shape_synset, shape_md5,
            'model.obj'),
        # 02958343/1a1de15e572e039df085b75b20c2db33/model.obj
        g_syn_images_num_per_CAD)
        for shape_md5 in shape_md5_list]

    return shape_list


def load_one_category_shape_views(synset):
    '''
    @input:
        shape synset
    @output:
        samples of viewpoints (plus distances) from pre-generated file,
        each element of view_params is a list of
        azimuth,elevation,tilt angles and distance
    '''
    # return shape_synset_view_params
    if not os.path.exists(g_view_distribution_files[synset]):
        print('Failed to read view distribution files from %s for synset %s' %
              (g_view_distribution_files[synset], synset))
        exit()

    view_params = open(g_view_distribution_files[synset]).readlines()
    view_params = [
        [float(x)
            for x in line.strip().split(' ')]
        for line in view_params]

    return view_params


def render_one_category_model_views(shape_list, view_params):
    '''
    @input:
        shape_list and view_params as output of
        load_one_category_shape_list/views
    @output:
        save rendered images to g_syn_images_folder/<synset>/<md5>/xxx.png
    '''
    tmp_dirname = tempfile.mkdtemp(dir=g_data_folder, prefix='tmp_view_')
    if not os.path.exists(tmp_dirname):
        os.mkdir(tmp_dirname)

    print('Generating rendering commands...')
    commands = []
    L = list(np.loadtxt(model_list, dtype='str'))
    for shape_synset, shape_md5, shape_file, _ in shape_list:
        if shape_md5 not in L:
            continue
        
        tmp = tempfile.NamedTemporaryFile(dir=tmp_dirname, delete=False)
        # write tmp view file
        for i in range(g_syn_images_num_per_CAD):
            paramId = random.randint(0, len(view_params)-1)
            tmp_string = b'%f %f %f %f %f\n' % (
                view_params[paramId][0],
                view_params[paramId][1],
                view_params[paramId][2],
                max(0.01, view_params[paramId][3]),
                view_params[paramId][4])
            tmp.write(tmp_string)
        tmp.close()
        #a = '> /dev/null 2>&1'
        a = ''
        command = ('%s %s --background --python %s -- %s %s %s %s %s' + a) % (
            g_blender_executable_path,
            g_blank_blend_file_path,
            os.path.join(BASE_DIR, 'render_model_views.py'),
            shape_file,
            shape_synset,
            shape_md5,
            tmp.name,
            os.path.join(g_syn_images_folder, shape_synset, shape_md5))

        commands.append(command)

    print('done (%d commands)!' % (len(commands)))
    print('Rendering, it takes long time...')

    report_step = 100
    if not os.path.exists(os.path.join(g_syn_images_folder, shape_synset)):
        os.mkdir(os.path.join(g_syn_images_folder, shape_synset))
    pool = Pool(g_syn_rendering_thread_num)
    for idx, return_code in enumerate(pool.imap(partial(call, shell=True), commands)):
        print('[%s] Rendering command %d of %d' % (
            datetime.datetime.now().time(), idx, len(L)))

        if return_code != 0:
            print('Rendering command %d of %d (\"%s\") failed' % (
                idx, len(shape_list), commands[idx]))

    shutil.rmtree(tmp_dirname)

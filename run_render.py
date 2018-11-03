#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
RENDER_ALL_SHAPES
@brief:
    render all shapes of PASCAL3D 12 rigid object classes
'''

import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *
from render_helper import *

if __name__ == '__main__':
    if not os.path.exists(g_syn_images_folder):
        os.mkdir(g_syn_images_folder)
    idx = 5
    synset = '02958343'
    print('%d: %s, %s\n' % (idx, synset, g_shape_names[idx]))
    shape_list = load_one_category_shape_list(synset)
    view_params = load_one_category_shape_views(synset)
    t = time.time()
    print(t)
    render_one_category_model_views(shape_list, view_params)
    print(time.time() - t)

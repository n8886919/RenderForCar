import bpy
import sys
import time
import numpy as np

scene = bpy.data.scenes['Scene']
scene.cycles.device = 'GPU'
scene.cycles.film_transparent = 1
scene.cycles.max_bounces = 4
scene.cycles.min_bounces = 1
#scene.cycles.samples = 32  # Time: 00:00.83
#scene.cycles.samples = 512  #  00:04.76

scene.use_nodes = True

# clear default nodes
'''
for n in scene.node_tree.nodes:
    scene.node_tree.nodes.remove(n)

view_node = scene.node_tree.nodes.new('CompositorNodeViewer')
view_node.use_alpha = True
RL_node = scene.node_tree.nodes.new('CompositorNodeRLayers')
scene.node_tree.links.new(RL_node.outputs[0], view_node.inputs[0])
'''
scene.render.engine = 'CYCLES'
# ('BLENDER_EEVEE', 'BLENDER_OPENGL', 'CYCLES')
scene.render.tile_x = 512
scene.render.tile_y = 512
scene.render.layers[0].cycles.use_denoising = True

world = bpy.data.worlds['World']
world.light_settings.use_ambient_occlusion = True
world.use_nodes = True

# set environment texture
env_node = world.node_tree.nodes.new('ShaderNodeTexEnvironment')
background_node = world.node_tree.nodes.get('Background')
world.node_tree.links.new(env_node.outputs[0], background_node.inputs[0])


bpy.data.objects['Cube'].select = True
bpy.ops.object.delete()

#env_node = world.node_tree.nodes.get('Environment Texture')
env_node.image = bpy.data.images.load(filepath='/home/nolan/Desktop/1.jpg')
env_node.interpolation = 'Smart'  # {'Linear', 'Closest', 'Cubic', 'Smart'}
env_node.projection = 'EQUIRECTANGULAR'  # {'EQUIRECTANGULAR', 'MIRROR_BALL'}

# import model and chande material properties
mdl = '/home/nolan/Desktop/02958343/1a1de15e572e039df085b75b20c2db33/model.obj'
bpy.ops.import_scene.obj(filepath=mdl)

for obj in bpy.data.objects:
    obj.select = False  # safe to un-select first, all objects.
    if obj.type == 'MESH':
        #obj.select = True
        obj.data.use_auto_smooth = 0


for mtl in bpy.data.materials:
    mtl.use_nodes = 1
    for n in bpy.data.materials[mtl.name].node_tree.nodes:
        bpy.data.materials[mtl.name].node_tree.nodes.remove(n)
    n1 = bpy.data.materials[mtl.name].node_tree.nodes.new('ShaderNodeBsdfPrincipled')
    n1.inputs[0].default_value = np.random.rand(4)  # (R, G, B, A)
    n1.inputs[4].default_value = np.random.randint(2)
    n1.inputs[7].default_value = np.random.rand()
    n1.inputs[12].default_value = np.random.rand()
    n1.inputs[13].default_value = np.random.rand()
    n2 = bpy.data.materials[mtl.name].node_tree.nodes.new('ShaderNodeOutputMaterial')
    bpy.data.materials[mtl.name].node_tree.links.new(n1.outputs[0], n2.inputs[0])

camObj = bpy.data.objects['Camera'].location = [1.0, -1.0, 0.65]
'''
bpy.ops.object.select_by_type(type='LAMP')
bpy.ops.object.delete(use_global=False)

bpy.ops.object.lamp_add(type='POINT', location=(2, 0, 2))
light_nodes = bpy.data.objects['Point'].data.node_tree.nodes
light_nodes['Emission'].inputs['Strength'].default_value = 100
light_nodes['Emission'].inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
'''
#scene.render.filepath = '/home/nolan/Desktop/test.png'
#bpy.ops.render.render(write_still=True)
t = time.time()
bpy.ops.render.render()
pixels = bpy.data.images['Viewer Node'].pixels

'''
blender /home/nolan/Desktop/RenderForCar/blank.blend --background \
--python /home/nolan/Desktop/RenderForCar/blender_cycles_test.py
'''

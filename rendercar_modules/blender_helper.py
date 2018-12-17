import bpy
import math
import numpy as np
import os
import sys

from global_variables import *

sys.path.append(g_ros_path)
sys.path.append(g_python_env_path)
sys.path.append(g_python_env_path2)

import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Int16MultiArray

def camPosToQuaternion(cx, cy, cz):
    camDist = math.sqrt(cx * cx + cy * cy + cz * cz)
    cx = cx / camDist
    cy = cy / camDist
    cz = cz / camDist
    axis = (-cz, 0, cx)
    angle = math.acos(cy)
    a = math.sqrt(2) / 2
    b = math.sqrt(2) / 2
    w1 = axis[0]
    w2 = axis[1]
    w3 = axis[2]
    c = math.cos(angle / 2)
    d = math.sin(angle / 2)
    q1 = a * c - b * d * w1
    q2 = b * c + a * d * w1
    q3 = a * d * w2 + b * d * w3
    q4 = -b * d * w2 + a * d * w3
    return (q1, q2, q3, q4)


def quaternionFromYawPitchRoll(yaw, pitch, roll):
    c1 = math.cos(yaw / 2.0)
    c2 = math.cos(pitch / 2.0)
    c3 = math.cos(roll / 2.0)
    s1 = math.sin(yaw / 2.0)
    s2 = math.sin(pitch / 2.0)
    s3 = math.sin(roll / 2.0)
    q1 = c1 * c2 * c3 + s1 * s2 * s3
    q2 = c1 * c2 * s3 - s1 * s2 * c3
    q3 = c1 * s2 * c3 + s1 * c2 * s3
    q4 = s1 * c2 * c3 - c1 * s2 * s3
    return (q1, q2, q3, q4)


def camPosToQuaternion(cx, cy, cz):
    q1a = 0
    q1b = 0
    q1c = math.sqrt(2) / 2
    q1d = math.sqrt(2) / 2
    camDist = math.sqrt(cx * cx + cy * cy + cz * cz)
    cx = cx / camDist
    cy = cy / camDist
    cz = cz / camDist
    t = math.sqrt(cx * cx + cy * cy)
    tx = cx / t
    ty = cy / t
    yaw = math.acos(ty)
    if tx > 0:
        yaw = 2 * math.pi - yaw
    pitch = 0
    tmp = min(max(tx*cx + ty*cy, -1), 1)
    #roll = math.acos(tx * cx + ty * cy)
    roll = math.acos(tmp)
    if cz < 0:
        roll = -roll
    #print("%f %f %f" % (yaw, pitch, roll))
    q2a, q2b, q2c, q2d = quaternionFromYawPitchRoll(yaw, pitch, roll)
    q1 = q1a * q2a - q1b * q2b - q1c * q2c - q1d * q2d
    q2 = q1b * q2a + q1a * q2b + q1d * q2c - q1c * q2d
    q3 = q1c * q2a - q1d * q2b + q1a * q2c + q1b * q2d
    q4 = q1d * q2a + q1c * q2b - q1b * q2c + q1a * q2d
    return (q1, q2, q3, q4)


def camRotQuaternion(cx, cy, cz, theta):
    theta = theta / 180.0 * math.pi
    camDist = math.sqrt(cx * cx + cy * cy + cz * cz)
    cx = -cx / camDist
    cy = -cy / camDist
    cz = -cz / camDist
    q1 = math.cos(theta * 0.5)
    q2 = -cx * math.sin(theta * 0.5)
    q3 = -cy * math.sin(theta * 0.5)
    q4 = -cz * math.sin(theta * 0.5)
    return (q1, q2, q3, q4)


def quaternionProduct(qx, qy):
    a = qx[0]
    b = qx[1]
    c = qx[2]
    d = qx[3]
    e = qy[0]
    f = qy[1]
    g = qy[2]
    h = qy[3]
    q1 = a * e - b * f - c * g - d * h
    q2 = a * f + b * e + c * h - d * g
    q3 = a * g - b * h + c * e + d * f
    q4 = a * h + b * g - c * f + d * e
    return (q1, q2, q3, q4)


def obj_centened_camera_pos(dist, azimuth_deg, elevation_deg):
    phi = float(elevation_deg) / 180 * math.pi
    theta = float(azimuth_deg) / 180 * math.pi
    x = (dist * math.cos(theta) * math.cos(phi))
    y = (dist * math.sin(theta) * math.cos(phi))
    z = (dist * math.sin(phi))
    return (x, y, z)


def init_render_engine(film_transparent=True, denoising=True):
    scene = bpy.data.scenes['Scene']

    scene.render.engine = 'CYCLES'
    scene.render.tile_x = 512
    scene.render.tile_y = 512
    scene.render.resolution_x = 640
    scene.render.resolution_y = 480
    #scene.render.image_settings.compression = 100
    scene.render.resolution_percentage = 100
    #scene.render.use_shadows = False
    #scene.render.use_raytrace = 0#True
    scene.render.layers[0].cycles.use_denoising = denoising

    scene.cycles.device = 'GPU'
    scene.cycles.max_bounces = 4
    scene.cycles.min_bounces = 1
    #bpy.ops.cycles.use_shading_nodes = True
    scene.cycles.film_transparent = film_transparent

    # init_background_node():
    world = bpy.data.worlds['World']
    #world.light_settings.use_ambient_occlusion = True
    world.use_nodes = True
    env_node = world.node_tree.nodes.new('ShaderNodeTexEnvironment')
    background_node = world.node_tree.nodes.get('Background')
    world.node_tree.links.new(env_node.outputs[0], background_node.inputs[0])


def set_render_engine(denoising_strength=0.5, samples=128):
    scene = bpy.data.scenes['Scene']
    scene.render.layers[0].cycles.denoising_strength = denoising_strength
    scene.cycles.samples = samples


def init_ros_node():
    scene = bpy.data.scenes['Scene']
    scene.use_nodes = True
    '''
    for n in scene.node_tree.nodes:
        scene.node_tree.nodes.remove(n)
    '''
    view_node = scene.node_tree.nodes.new('CompositorNodeViewer')
    view_node.use_alpha = True
    #RL_node = scene.node_tree.nodes.new('CompositorNodeRLayers')
    RL_node = scene.node_tree.nodes.get('Render Layers')
    scene.node_tree.links.new(RL_node.outputs[0], view_node.inputs[0])
    scene.node_tree.links.new(RL_node.outputs[1], view_node.inputs[1])

    rospy.init_node('blender_publisher', anonymous=True)
    #pub = rospy.Publisher('/blender/image', Float32MultiArray, queue_size=10)
    pub = rospy.Publisher('/blender/image', Int16MultiArray, queue_size=10)
    return pub


def set_background(path='test1.jpg', interpolation='Smart', projection='EQUIRECTANGULAR'):
    env_node = bpy.data.worlds['World'].node_tree.nodes.get('Environment Texture')
    env_node.image = bpy.data.images.load(filepath=path)
    env_node.interpolation = interpolation  # {'Linear', 'Closest', 'Cubic', 'Smart'}
    env_node.projection = projection  # {'EQUIRECTANGULAR', 'MIRROR_BALL'}


def remove_all_mesh():
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()


def remove_cube():
    bpy.ops.object.select_all(action='TOGGLE')
    for obj in bpy.data.objects:
        if obj.name == 'Cube':
            bpy.data.objects['Cube'].select = True
            bpy.ops.object.delete()


def import_obj(mdl='/home/nolan/Desktop/RenderForCar/datasets/shapenetcore/02958343/1a1dcd236a1e6133860800e6696b8284/model.obj'):
    bpy.ops.import_scene.obj(filepath=mdl)
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.data.use_auto_smooth = 0


def material_randomize():
    materials = bpy.data.materials
    for mtl in materials:
        mtl.use_nodes = 1
        for n in materials[mtl.name].node_tree.nodes:
            materials[mtl.name].node_tree.nodes.remove(n)
        n1 = materials[mtl.name].node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        n1.inputs[0].default_value = np.random.rand(4)  # (R, G, B, A)
        n1.inputs[4].default_value = np.random.randint(2)
        n1.inputs[7].default_value = np.random.rand() * 0.3
        n1.inputs[12].default_value = np.random.rand()
        n1.inputs[13].default_value = np.random.rand()
        n2 = materials[mtl.name].node_tree.nodes.new('ShaderNodeOutputMaterial')
        materials[mtl.name].node_tree.links.new(n1.outputs[0], n2.inputs[0])


def delete_light():
    bpy.ops.object.select_by_type(type='LAMP')
    bpy.ops.object.delete(use_global=False)


def set_environment_light(energy_lowbound=0, energy_highbound=1.0):
    bpy.context.space_data.context = 'WORLD'
    light = bpy.context.scene.world.light_settings
    light.use_environment_light = True
    light.environment_energy = np.random.uniform(energy_lowbound, energy_highbound)
    light.environment_color = 'PLAIN'


def set_light(xyz=(0, 0, 1), strength=100, rgba=(1.0, 1.0, 1.0, 1.0)):
    bpy.ops.object.lamp_add(type='POINT', location=xyz)
    light_nodes = bpy.data.objects['Point'].data.node_tree.nodes
    light_nodes['Emission'].inputs['Strength'].default_value = strength
    light_nodes['Emission'].inputs['Color'].default_value = rgba


def set_camera_from_angle(azi, ele, rho, theta=0):
    cx, cy, cz = obj_centened_camera_pos(rho, azi, ele)
    q1 = camPosToQuaternion(cx, cy, cz)
    q2 = camRotQuaternion(cx, cy, cz, theta)
    q = quaternionProduct(q2, q1)
    set_camera((cx, cy, cz), q)


def set_camera(xyz=(1.0, -1.0, 0.65), quaternion=None):
    # camObj.data.lens_unit = 'FOV'
    # camObj.data.angle = 0.2
    camObj = bpy.data.objects['Camera']
    camObj.location = xyz
    if quaternion is not None:
        camObj.rotation_mode = 'QUATERNION'
        camObj.rotation_quaternion = quaternion


def render(path=None, pub_node=None, label=(0, 0)):
    write = False
    if path is not None:
        bpy.data.scenes['Scene'].render.filepath = path
        write = True
    bpy.ops.render.render(write_still=write)

    if pub_node is not None:
        data = np.array(bpy.data.images['Viewer Node'].pixels)
        data= np.power(data, 1/2.2) * 255.
        data = np.clip(np.around(data), 0, 255).astype('int')

        ros_array = Int16MultiArray()
        ros_array.layout.dim.append(MultiArrayDimension())
        #ros_array.layout.dim[0].label = 'ros_azi%d_ele%d.png' % (azi, ele)
        ros_array.data = data
   
        pub_node.publish(ros_array)


def show_available_node_name():
    # list available node name
    subclasses = bpy.types.ShaderNode.__subclasses__()
    nodes = [node.bl_rna.identifier for node in subclasses]
    for node in nodes:
        print(node)


def test():
    init_render_engine(film_transparent=True)
    remove_all_mesh()
    set_background(path='/home/nolan/Desktop/RenderForCar/test/2.jpg')
    delete_light()
    import_obj(mdl='/home/nolan/Desktop/RenderForCar/datasets/shapenetcore/02958343/1a1dcd236a1e6133860800e6696b8284/model.obj')
    material_randomize()
    set_camera_from_angle(30, 30, 1.5)
    render(path='/home/nolan/Desktop/RenderForCar/module/test.jpg')


if __name__ == '__main__':
    test()

'''
blender /home/$USER/Desktop/RenderForCar/blank.blend --background \
--python /home/$USER/Desktop/RenderForCar/module/blender_helper.py

import sys
sys.path.append('/home/nolan/Desktop/RenderForCar/module')
from blender_helper import *
init_render_engine(film_transparent=True)
init_ros_node()
test()
bpy.ops.object.select_by_type(type='Camera', action='TOGGLE')
bpy.ops.object.delete()
bpy.ops.object.camera_add()
test()
'''

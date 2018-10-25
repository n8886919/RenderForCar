bpy.context.scene.render.engine = 'CYCLES'
bpy.data.scenes['Scene'].cycles.device = 'GPU'
bpy.data.scenes['Scene'].render.filepath = '/home/nolan/Desktop/test.png'
bpy.data.scenes['Scene'].render.tile_x = 512
bpy.data.scenes['Scene'].render.tile_y = 512
bpy.data.scenes['Scene'].render.layers[0].cycles.use_denoising = True

bpy.data.scenes['Scene'].cycles.max_bounces = 4
bpy.data.scenes['Scene'].cycles.min_bounces = 1

bpy.data.scenes['Scene'].cycles.samples = 32  # Time: 00:00.83
bpy.data.scenes['Scene'].cycles.samples = 512  #  00:04.76

bpy.ops.object.select_by_type(type='LAMP')
bpy.ops.object.delete(use_global=False)

bpy.data.objects['Cube'].select = True
bpy.ops.object.delete()
bpy.ops.import_scene.obj(
    filepath='/home/nolan/Desktop/02958343/1a0bc9ab92c915167ae33d942430658c/model.obj')

camObj = bpy.data.objects['Camera']
camObj.location = [1, -1, 0.8]

bpy.ops.object.lamp_add(location=(2, 0.0, 1.0))

light_nodes = bpy.data.objects['Point'].data.node_tree.nodes
light_nodes['Emission'].inputs['Strength'].default_value = 100
light_nodes['Emission'].inputs['Color'].default_value = (0.2, 0.2, 0, 1.0)

bpy.data.worlds['World'].light_settings.use_ambient_occlusion = True

bpy.ops.render.render( write_still=True )

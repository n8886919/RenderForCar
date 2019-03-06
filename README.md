# RenderForCar
![](https://i.imgur.com/BQvjIBh.jpg)

## Quick Test
1. git clone https://github.com/n8886919/RenderForCar.git
2. Install blender2.79
```sh
cd CLONE_FOLDER
export PYTHONPATH=$PYTHONPATH:CLONE_FOLDER
blender blank.blend --python rendercar_modules/blender_helper.py
```
Generate an image
CLONE_FOLDER/test/test_result.png
![](https://i.imgur.com/45B9lFn.png)
## Generate Dataset
sh CLONE_FOLDER/datasets/get_sun2012pascalformat.sh
sh CLONE_FOLDER/datasets/get_shapenet.sh
edit global_variables.py
python run_render.py



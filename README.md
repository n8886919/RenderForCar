# RenderForCar
![](https://i.imgur.com/BQvjIBh.jpg)

## Quick Test
1. git clone https://github.com/n8886919/RenderForCar.git
2. Install blender2.79
then
```sh
cd CLONE_FOLDER
export PYTHONPATH=$PYTHONPATH:CLONE_FOLDER
blender blank.blend --python rendercar_modules/blender_helper.py
```
Generate an image
CLONE_FOLDER/test/test_result.png
![](https://i.imgur.com/45B9lFn.png)
## Generate Dataset
1. sh CLONE_FOLDER/datasets/get_sun2012pascalformat.sh
2. sh CLONE_FOLDER/datasets/get_shapenet.sh
3. edit global_variables.py
4. python run_render.py



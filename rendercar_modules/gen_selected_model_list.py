import numpy as np
import os

selected_model_path = '704'
L = []
for img_name in os.listdir(selected_model_path):
	L.append(img_name.split('.')[0])

np.savetxt('../../selected_704models.txt', L, fmt='%s')

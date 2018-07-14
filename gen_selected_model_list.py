import numpy as np
import os

selected_model_path = './selected_model'
L = []
for img_name in os.listdir(selected_model_path):
	L.append(img_name.split('.')[0])

np.savetxt('selected_model.txt', L, fmt='%s')

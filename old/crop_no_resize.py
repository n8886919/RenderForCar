import numpy as np
import os
import queue
import sys
import threading
import multiprocessing as mp
from PIL import Image
import xml.etree.cElementTree as ET
from global_variables import *

syn_size = [480, 270]
thread_num = 8

selected_model_list = list(np.loadtxt('selected_model.txt', dtype='str'))
print(len(selected_model_list))
car_folder = os.path.join(g_syn_images_folder, g_shape_synsets[5])
sun_img_path = os.path.join(g_sun2012pascalformat_root_folder, 'JPEGImages')
sun_anno_path = os.path.join(g_sun2012pascalformat_root_folder, 'Annotations')

data_path = '/home/showay/Desktop/darknet/48x27_15cls'
train_img_path = os.path.join(data_path, 'train_img')
valid_img_path = os.path.join(data_path, 'valid_img')
train_txt_path = os.path.join(data_path, 'train.txt')
valid_txt_path = os.path.join(data_path, 'valid.txt')

if not os.path.exists(data_path): os.mkdir(data_path)
if not os.path.exists(train_img_path): os.mkdir(train_img_path)
if not os.path.exists(valid_img_path): os.mkdir(valid_img_path)

counter=0	
threads = []
threadLock = threading.Lock()
CADqueue = queue.Queue(len(selected_model_list))
traintxt_q = queue.Queue()
validtxt_q = queue.Queue()
'''
class crop_thread(threading.Thread):
	def __init__(self, threadID, threadLock, q):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.q = q
		
	def run(self):
		while not CADqueue.empty():
			CAD_name = self.q.get()
			crop_one_CAD(CAD_name)
'''		
		
def main():
	for CAD_name in selected_model_list:
		CADqueue.put(CAD_name)

	for ID in range(thread_num):
		t = mp.Process(target=crop_one_CAD)
		t.start()
		threads.append(t)
		
	for t in threads:
		t.join()
	'''
	traintxt = []
	validtxt = []
	while not traintxt_q.empty():
		traintxt.ppend(traintxt_q.get())
	while not validtxt_q.empty():
		validtxt.append(validtxt_q.get())

	print("All Thread Finish")
	np.savetxt(train_txt_path, traintxt, fmt='%s')	
	np.savetxt(valid_txt_path, validtxt, fmt='%s')	
	'''
	
	
def crop_one_CAD():
	global counter
	while not CADqueue.empty():
		CAD_name = CADqueue.get()
		CAD_folder = os.path.join(car_folder, CAD_name)
		train = True if np.random.sample()<0.95 else False # train or valid
		for img_name in os.listdir(CAD_folder):
		############### Load img ###############			
			img_path = os.path.join(CAD_folder, img_name)
			fg = Image.open(img_path, 'r').resize( (syn_size[0], syn_size[1]) )#resize fg
			syn_img = rand_select_bg().resize( (syn_size[0], syn_size[1]) ) 
			tmp_img = Image.new('RGBA', (syn_size[0], syn_size[1]))
		
		########### Move and Resize ###########
			rs_cst = np.random.sample() + 0.5 # 0.5x~1.5x
			fg = fg.crop(fg.getbbox())
			fg = fg.resize((int(rs_cst*fg.size[0]),int(rs_cst*fg.size[1])), Image.ANTIALIAS) 
			bbox = fg.getbbox()
			#move_x = int(np.random.sample() * syn_size[0] - fg.size[0]/2) # -0.5b ~ 160+0.5b
			#move_y = int(np.random.sample() * syn_size[1] - fg.size[1]/2) # -0.5b ~ 90+0.5b
			bbox_w = bbox[2]-bbox[0]
			bbox_h = bbox[3]-bbox[1]
			move_x = int(np.random.sample() * (syn_size[0] - bbox_w))-bbox[0] # left-top corner
			move_y = int(np.random.sample() * (syn_size[1] - bbox_h))-bbox[1] # left-top corner			
			tmp_img.paste(fg, (move_x, move_y))
			bbox_centx = move_x + bbox[0] + 0.5*bbox_w
			bbox_centy = move_y + bbox[1] + 0.5*bbox_h
		
		################ Merge ################
			tmp_img.load()
			syn_img.paste(tmp_img, mask=tmp_img.split()[3])
			'''
		################# Label #################
			labels = []
			cls = [int(img_name.split('label')[1].split('_')[0])]
			labels.extend(cls)

			bbox_yolofmt = [bbox_centx/syn_size[0], bbox_centy/syn_size[1],
                            bbox_w/syn_size[0], bbox_h/syn_size[1]]
			labels.extend(bbox_yolofmt)
			labels_file_name = CAD_name + img_name.split('.')[0] + '.txt'
			labels_path = train_img_path if train else valid_img_path
			np.savetxt(os.path.join(labels_path, labels_file_name), [labels], fmt='%d %.6f %.6f %.6f %.6f')

		############### Save img ###############
			if train:
				syn_img_path = os.path.join(train_img_path, (CAD_name + img_name.split('.')[0] + '.jpg'))
				traintxt_q.put(syn_img_path)
			else:
				syn_img_path = os.path.join(valid_img_path, (CAD_name + img_name.split('.')[0] + '.jpg'))
				validtxt_q.put(syn_img_path)
			syn_img.save(syn_img_path, "jpeg")	
			
		##########################################
			fg.close()
			tmp_img.close()
			syn_img.close()

		############### Lock start ###############	
			counter += 1
			print('\r', counter, ' ', CAD_name, img_name, end=' ')
		################ Lock end ################
			#break	
			'''
			
			
def rand_select_bg():	
	while True:
		detected = False
		img = np.random.choice(os.listdir(sun_img_path))
		img_name = (img.split('.')[0]).split('/')[-1]
		#print(bg)
		#print(bg_name)
		try:
			img_xml_path = os.path.join(sun_anno_path, (img_name+'.xml'))
			img_xml = ET.ElementTree(file=img_xml_path)
			root = img_xml.getroot()
			for child in root:
				if child.tag == 'object':
					for sub_child in child:
						if sub_child.tag == 'name':
							text = sub_child.text
							if ('car' in text or 'van' in text or 'truck' in text):
								detected = True
								break	
							'''
							if sub_child.text[1:-1] in delete_key_worlds: 
								detected = True
								break
							'''
					if detected: break
		except:
			detected = True
		if not detected:
			selected_bg = Image.open(os.path.join(sun_img_path ,img))
			break

	return selected_bg
	
	
if __name__ == '__main__':
	main()



		
			


			
			

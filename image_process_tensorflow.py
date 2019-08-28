import os
import sys
import shutil
import time
import numpy as np
import step_1
import step_2
import step_3
import step_5
import step_6

# This line need to change your upper layer path of image folder.
input_path = ''
# This line is the output path after the data processing is completed.
output_path = ''
# This line need to change your original image folder.
DataSet_Folder = ['']

# train, test, validation
split_rate = [0.94, 0.04, 0.02]

def check_folder(folder_path):
	if os.path.isdir(folder_path):
		shutil.rmtree(folder_path)
		time.sleep(0.2)
		os.makedirs(folder_path)
	else:
		os.makedirs(folder_path)

def step_4_create_label_map(className):
	with open(output_path+'object_detection.pbtxt','w') as f:
		for i,l in enumerate(np.array(className)):
			f.write('item {\n  id : %s\n  name : \'%s\'\n}\n' % (i+1, l))
	print('...create label map complete!...\n')

if __name__ == '__main__':

	if not np.sum(split_rate) == 1:
		print('split rate error!')
		sys.exit()

	check_folder(output_path)

	className = []
	for f in DataSet_Folder:
		className.append(f.split('_DataSet')[0])
	
	className = np.array(className , dtype=np.str)

	step_1.file_Rename(DataSet_Folder, input_path, className)

	step_2.file_split(DataSet_Folder, input_path, output_path, split_rate)

	step_3.modify_xml(className, output_path)
	
	step_4_create_label_map(className)
	
	step_5.xml_to_csv(output_path)
	
	step_6.generate_tfrecord(className, output_path)


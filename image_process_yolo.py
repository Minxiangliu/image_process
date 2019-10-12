import shutil
import time
import sys
import os
import numpy as np
import step_1
import transferYOLO


# This line need to change your upper layer path of image folder.
input_path = ''
# This line is the output path after the data processing is completed.
output_path = ''
# This line need to change your original image folder.
DataSet_Folder = ['']

# train, test, validation
split_rate = [0.9, 0.1]


def check_folder(folder_path):
	if os.path.isdir(folder_path):
		shutil.rmtree(folder_path)
		time.sleep(0.2)
		os.makedirs(folder_path)
	else:
		os.makedirs(folder_path)


if __name__ == '__main__':

	cfg_obj_names = "obj.names"
	cfg_obj_data = "obj.data"

	if not np.sum(split_rate) == 1:
		print('split rate error!')
		sys.exit()

	className = []
	for f in DataSet_Folder:
		if len(f.split('_DataSet')) == 1:
			print('DataSet_Folder file name error!')
			sys.exit()
		else:
			className.append(f.split('_DataSet')[0])
	className = np.array(className , dtype=np.str)

	step_1.file_Rename(DataSet_Folder, input_path, className)

	output_dir = ['train','test','validation']
	if os.path.isdir(output_path):
		shutil.rmtree(output_path)
	for i in range(len(split_rate)):
		check_folder(output_path+output_dir[i])
	check_folder(output_path+'cfg')
	check_folder(output_path+'weights')


	transferYOLO.transfer(split_rate=split_rate, 
		input_path=input_path, output_path=output_path, 
		DataSet_Folder=DataSet_Folder, className=className)


	with open(output_path+'cfg/'+cfg_obj_data, 'w') as the_file:
		the_file.write("classes = " + str(len(className)) + "\n")
		the_file.write("train = " + output_path+'cfg/' + "train.txt\n")
		the_file.write("valid = " + output_path+'cfg/' + "test.txt\n")
		the_file.write("names = " + output_path+'cfg/' + "obj.names\n")
		the_file.write("backup = " + output_path+ "weights/")
	the_file.close()

	with open(output_path+'cfg/'+cfg_obj_names, 'w') as the_file:
		for n in className:
			the_file.write(n + "\n")

	the_file.close()




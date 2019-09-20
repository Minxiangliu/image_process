import os
import shutil
from sklearn.model_selection import train_test_split
import image_process_tensorflow
import sys


def file_split(DataSet_Folder, input_path, output_path, split_rate):
	train_file_Number=0
	test_file_Number=0
	validation_file_Number = 0

	if len(split_rate) == 3:
		folder_ = ['train', 'test', 'validation']
	elif len(split_rate) == 2:
		folder_ = ['train', 'test']

	for f in folder_:
		image_process_tensorflow.check_folder(output_path+f)

	for p in DataSet_Folder:
		xml_fileName = []
		path = input_path+p+'/'
		list_dir = os.listdir(path)
		for l in list_dir:
			if l.endswith('xml'):
				xml_fileName.append(l.split('.',2)[0])

		if len(folder_) == 3:
			train, test = train_test_split(xml_fileName, test_size=split_rate[1], random_state=1)
			train, validation = train_test_split(train, test_size=split_rate[2], random_state=1)
			folder_parting = [train, test, validation]
		elif len(folder_) == 2:
			train, test = train_test_split(xml_fileName, test_size=split_rate[1], random_state=1)
			folder_parting = [train, test]

		for i, f_p in enumerate(folder_parting):
			for fileN in f_p:
				shutil.copyfile(path + fileN + '.xml', output_path + folder_[i] +'/' + fileN +'.xml')
				shutil.copyfile(path + fileN + '.jpg', output_path + folder_[i] +'/' + fileN +'.jpg')

			print('{} folder move image and xml individually file for {}.'.format(folder_[i],len(folder_parting[i])))

	print('...File split complete!...\n')
import os
import shutil
from sklearn.model_selection import train_test_split
import image_process_tensorflow
import sys

folder_ = ['train', 'test', 'validation']

def file_split(DataSet_Folder, input_path, output_path, split_rate):
	train_file_Number=0
	test_file_Number=0
	validation_file_Number = 0

	for f in folder_:
		image_process_tensorflow.check_folder(output_path+f)

	for p in DataSet_Folder:
		xml_fileName = []
		path = input_path+p+'/'
		list_dir = os.listdir(path)
		for l in list_dir:
			if l.endswith('xml'):
				xml_fileName.append(l.split('.',2)[0])

		train, test = train_test_split(xml_fileName, test_size=split_rate[1], random_state=1)
		train, validation = train_test_split(train, test_size=split_rate[2], random_state=1)

		for tr in train:
			shutil.copyfile(path + tr + '.xml', output_path + 'train/' + tr +'.xml')
			shutil.copyfile(path + tr + '.jpg', output_path + 'train/' + tr +'.jpg')

		for te in test:
			shutil.copyfile(path + te + '.xml', output_path + 'test/' + te +'.xml')
			shutil.copyfile(path + te + '.jpg', output_path + 'test/' + te +'.jpg')

		for va in validation:
			shutil.copyfile(path + va + '.xml', output_path + 'validation/' + va +'.xml')
			shutil.copyfile(path + va + '.jpg', output_path + 'validation/' + va +'.jpg')			

		print(p, 'train file move', len(train))
		print(p, 'test file move', len(test))
		print(p, 'validation file move', len(validation),'\n')
		train_file_Number+=len(train)
		test_file_Number+=len(test)
		validation_file_Number+=len(validation)

	print('train file number=',train_file_Number, ',All file display=',train_file_Number*2)
	print('test file number=',test_file_Number, ',All file display=',test_file_Number*2)
	print('validation file number=',validation_file_Number, ',All file display=',validation_file_Number*2)
	print('...File split complete!...\n')
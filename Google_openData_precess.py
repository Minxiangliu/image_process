import numpy as np
import cv2
import os
import shutil
import time
import random
import pandas as pd
import sys
import time

# 請輸入總共輸出資料集的數量，預設None輸出原數量
output_image_number = None

cvs_path = ''
image_path = ''
output_path = ''
select_class_name = ''

def read_cvs_file():
	print('CSV file reading...')
	class_info_csv = np.loadtxt(cvs_path+'class_info.csv' ,dtype=np.str, delimiter=',')

	tr_pd = pd.read_csv(cvs_path+'train-annotations-bbox.csv')
	te_pd = pd.read_csv(cvs_path+'test-annotations-bbox.csv')
	va_pd = pd.read_csv(cvs_path+'validation-annotations-bbox.csv')
	tr_ = tr_pd.to_numpy()
	te_ = te_pd.to_numpy()
	va_ = va_pd.to_numpy()
	print('CSV file read done.')

	print('Concatenate data...')
	all_annotations_bbox_DataSet = np.concatenate((tr_[:,[0,2,4,5,6,7]], te_[:,[0,2,4,5,6,7]], va_[:,[0,2,4,5,6,7]]), axis=0).astype(np.str)

	print('class_info_csv search...')
	c_ = np.where(class_info_csv==select_class_name)
	if not len(c_[0]) == 0:
		return int(class_info_csv[c_[0][0]][2]), class_info_csv[c_[0][0]][1], all_annotations_bbox_DataSet
	else:
		return 0, None, None

def xml_write(object_txt, filename, img, path):
	line_1 = '<?xml version="1.0" ?><annotation>\n'
	line_2 = '\t<folder>DataSet_'+select_class_name+'</folder>\n'
	line_3 = '\t<filename>'+filename+'.jpg</filename>\n'
	line_4 = '\t<size>\n'
	line_5 = '\t\t<width>'+str(img[1])+'</width>\n'
	line_6 = '\t\t<height>'+str(img[0])+'</height>\n'
	line_7 = '\t\t<depth>'+str(img[2])+'</depth>\n'
	line_8 = '\t</size>\n'
	line_9 = '</annotation>'

	text = line_1+line_2+line_3+line_4+line_5+line_6+line_7+line_8+object_txt+line_9

	with open(path+filename+'.xml', 'w') as f:
		f.write(text)

def main(output_image_number):

	#讀取CVS檔案
	all_train_class_number, class_number_coding, all_annotations_bbox_DataSet = read_cvs_file()
	
	# 檢查輸出資料集是否小於等於總資料集
	if not output_image_number == None:
		if all_train_class_number < output_image_number:
			print('More than the number of Data sets!, The largest', all_train_class_number)
			sys.exit()
	elif output_image_number == None:
		output_image_number = all_train_class_number
			
	print('[\'{}\', \'{}\'] class is readying, output image {}.'.format(select_class_name, class_number_coding, output_image_number))

	# 檢查輸出路徑
	o_path = output_path+select_class_name+'_DataSet/'
	if os.path.isdir(o_path):
		shutil.rmtree(o_path)
		time.sleep(0.2)
		os.makedirs(o_path)
	else:
		os.makedirs(o_path)


	# 使用編碼名稱蒐尋影像名稱和bounding box
	print('bounding box search...')
	index = np.where(all_annotations_bbox_DataSet == class_number_coding)[0]
	if len(index) == 0:
		print('\'{}\' Not find in DataSet.'.format(select_class_name))
		sys.exit()
	else:
		image_annotations_bbox = all_annotations_bbox_DataSet[index]

	print('get image_annotations_bbox...')

	# 整理出影像檔案名稱
	imageName_list = np.unique(image_annotations_bbox[:,[0]], axis=0)
	imageName_list = imageName_list.ravel()
	np.random.shuffle(imageName_list)
	print('get imageName_list done...')

	
	folder = ['test/','validation/']
	for i in range(9):
		folder.append('train_0{}/'.format(i))


	# 拷貝影像集並產生出xml檔案
	# flg = 0
	print('Image and xml file generate...')
	for n,im_Name in enumerate(imageName_list):
		index = np.where(image_annotations_bbox==im_Name)[0]

		for f in folder:
			img = cv2.imread(image_path+f+im_Name+'.jpg')
			if not type(img) == type(None):
				new_image_path = image_path+f+im_Name+'.jpg'
				break

		if type(img)==type(None):
			print('Image not found!')
			sys.exit(0)

		# height, width, depth
		img_shape = img.shape
		object_txt = ''
		for i in index:
			XMin, XMax, YMin, YMax = image_annotations_bbox[i][2:]
			object_txt_1 = '\t<object>\n'
			object_txt_2 = '\t\t<name>'+select_class_name+'</name>\n'
			object_txt_3 = '\t\t<bndbox>\n'
			object_txt_4 = '\t\t\t<xmin>'+str(round(float(XMin)*img_shape[1]))+'</xmin>\n'
			object_txt_5 = '\t\t\t<ymin>'+str(round(float(YMin)*img_shape[0]))+'</ymin>\n'
			object_txt_6 = '\t\t\t<xmax>'+str(round(float(XMax)*img_shape[1]))+'</xmax>\n'
			object_txt_7 = '\t\t\t<ymax>'+str(round(float(YMax)*img_shape[0]))+'</ymax>\n'
			object_txt_8 = '\t\t</bndbox>\n'
			object_txt_9 = '\t</object>\n'

			object_txt += object_txt_1+object_txt_2+object_txt_3+object_txt_4+object_txt_5+object_txt_6+object_txt_7+object_txt_8+object_txt_9


		if n == output_image_number:
			break

		xml_write(object_txt, im_Name, img_shape, o_path)
		shutil.copyfile(new_image_path, o_path+im_Name+'.jpg')

	print('Done...')

if __name__ == '__main__':
	main(output_image_number=output_image_number)
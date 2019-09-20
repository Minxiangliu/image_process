import os
import shutil
import image_process_tensorflow

import sys

def file_Rename(Folder, input_path, className):
	for c_i,f in enumerate(Folder):
		xml_fileName = []
		img_fileName = []
		path = input_path+f+'/'
		fileName_list = sorted(os.listdir(path))

		for l in fileName_list:
			if l.endswith('xml'):
				xml_fileName.append(l)
			elif l.endswith('jpg') or l.endswith('JPG') or l.endswith('jpeg') or l.endswith('JPEG') or l.endswith('png') or l.endswith('PNG'):
				img_fileName.append(l)
		
		if len(img_fileName) > 0:
			for i, imgN in enumerate(img_fileName):
				im_out = path+className[c_i]+'_{}.jpg'.format(i+1)
				if not os.path.isfile(im_out):
					os.rename(path+imgN, im_out)
				

		if len(xml_fileName) > 0:
			for j, xmlN in enumerate(xml_fileName):
				xml_out = path+className[c_i]+'_{}.xml'.format(j+1)
				if not os.path.isfile(xml_out):
					os.rename(path+xmlN, xml_out)
				

		print('Rename folder:',f)

	print('Rename complete!...\n')

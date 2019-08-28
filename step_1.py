import os
import shutil
import image_process_tensorflow

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
				try:
					os.rename(path+imgN, path+className[c_i]+'_{}.jpg'.format(i+1))
				except Exception as e:
					pass
		if len(xml_fileName) > 0:
			for j, xmlN in enumerate(xml_fileName):
				try:
					os.rename(path+xmlN, path+className[c_i]+'_{}.xml'.format(j+1))
				except Exception as e:
					pass

		print('Rename folder:',f)

	print('Rename complete!...\n')

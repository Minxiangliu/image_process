import os
import numpy as np
from xml.dom import minidom

folder_ = ['train', 'test', 'validation']

def xml_write(xml_path, img_FileName, folder_new, className):
	dom = minidom.parse(xml_path)
	root = dom.documentElement

	folder = root.getElementsByTagName('folder')
	filename = root.getElementsByTagName('filename')
	path = root.getElementsByTagName('path')
	name = root.getElementsByTagName('name')

	for n in name:
		index = np.where(className==n.firstChild.data)
		for i in index[0]:
			BoxNumber[index[0][0]] += 1

	if len(path) > 0:
		path[0].firstChild.data = os.path.dirname(xml_path)+'/'+img_FileName
	
	
	folder[0].firstChild.data = folder_new
	filename[0].firstChild.data = img_FileName

	with open(xml_path,'w') as fh:
		dom.writexml(fh)


def modify_xml(className, output_path):
	global BoxNumber

	for f in folder_:
		print()
		BoxNumber = np.zeros(len(className), dtype=np.int)
		xml_file_name = []
		img_file_name = []
		path = output_path+f+'/'
		all_file_name = os.listdir(path)
		for l in all_file_name:
			if l.endswith('xml'):
				xml_file_name.append(l)
			elif l.endswith('jpg') or l.endswith('JPG') or l.endswith('jpeg') or l.endswith('JPEG') or l.endswith('png') or l.endswith('PNG'):
				img_file_name.append(l)

		for i, x in enumerate(xml_file_name):
			xml_write(path+x, img_file_name[i], f, className)

		print('%s folder:' % f)
		for j, b in enumerate(BoxNumber):
			print('%s box number: %s' % (className[j], b))
		
	
	print('...modify_xml complete!...\n')
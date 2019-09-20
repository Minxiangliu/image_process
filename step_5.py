import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import image_process_tensorflow
import numpy as np

def xml_to_csv_pre(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            for i in range(len(member)):
                if member[i].text == 'bndbox':
                    index = i
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[i][0].text),
                     int(member[i][1].text),
                     int(member[i][2].text),
                     int(member[i][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def xml_to_csv(output_path):
    output_dir = output_path+'data'
    image_process_tensorflow.check_folder(output_dir)

    for directory in ['train', 'test', 'validation']:
        image_path = os.path.join(output_path, '{}'.format(directory))

        if not os.path.exists(image_path):
            continue

        xml_df = xml_to_csv_pre(image_path)
        xml_df.to_csv(output_path + 'data/{}_labels.csv'.format(directory), index=None)
        print(directory,'folder successfully converted xml to csv.')
    print()
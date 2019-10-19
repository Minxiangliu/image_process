import os
import time
import shutil
import cv2
from xml.dom import minidom
import sys
import numpy as np
from sklearn.model_selection import train_test_split

def run(classList, classNumList,fileNamePath, outpath,labelGrep=""):

    img = cv2.imread(fileNamePath+'.jpg')
    if type(img) == None:
        print('image not find!')
        sys.exit()
    imgShape = img.shape

    img_h = imgShape[0]
    img_w = imgShape[1]

    labelXML = minidom.parse(fileNamePath+'.xml')
    labelName = []
    labelXmin = []
    labelYmin = []
    labelXmax = []
    labelYmax = []

    tmpArrays = labelXML.getElementsByTagName("filename")
    for elem in tmpArrays:
        filenameImage = elem.firstChild.data

    tmpArrays = labelXML.getElementsByTagName("name")
    for elem in tmpArrays:
        labelName.append(str(elem.firstChild.data))

    tmpArrays = labelXML.getElementsByTagName("xmin")
    for elem in tmpArrays:
        labelXmin.append(int(elem.firstChild.data))

    tmpArrays = labelXML.getElementsByTagName("ymin")
    for elem in tmpArrays:
        labelYmin.append(int(elem.firstChild.data))

    tmpArrays = labelXML.getElementsByTagName("xmax")
    for elem in tmpArrays:
        labelXmax.append(int(elem.firstChild.data))

    tmpArrays = labelXML.getElementsByTagName("ymax")
    for elem in tmpArrays:
        labelYmax.append(int(elem.firstChild.data))


    with open(outpath, 'w') as the_file:
        i = 0
        for className in labelName:
            if(className==labelGrep or labelGrep==""):
                classID = classList[className]
                classNumList[className] += 1
                x = (labelXmin[i] + (labelXmax[i]-labelXmin[i])/2) * 1.0 / img_w 
                y = (labelYmin[i] + (labelYmax[i]-labelYmin[i])/2) * 1.0 / img_h
                w = (labelXmax[i]-labelXmin[i]) * 1.0 / img_w
                h = (labelYmax[i]-labelYmin[i]) * 1.0 / img_h

                the_file.write(str(classID) + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + '\n')
                i += 1

    the_file.close()


def transfer(split_rate, input_path, output_path, DataSet_Folder, className, yolo=False):
    global classNumList

    print('className:',className)

    classList = {}
    classNumList = {}
    for i,c in enumerate(className):
        classList[c] = i
        classNumList[c] = 0


    if len(split_rate) == 3:
        folder_ = ['train', 'test', 'validation']
    elif len(split_rate) == 2:
        folder_ = ['train', 'test']


    for p in DataSet_Folder:
        fileName = []
        path = input_path+p+'/'
        list_dir = os.listdir(path)
        for l in list_dir:
            if yolo:
                if l.endswith('txt'):
                    fileName.append(l.split('.',2)[0])
            else:
                if l.endswith('xml'):
                    fileName.append(l.split('.',2)[0])

        if len(folder_) == 3:
            train, test = train_test_split(fileName, test_size=split_rate[1], random_state=1)
            train, validation = train_test_split(train, test_size=split_rate[2], random_state=1)
            folder_parting = [train, test, validation]
        elif len(folder_) == 2:
            train, test = train_test_split(fileName, test_size=split_rate[1], random_state=1)
            folder_parting = [train, test]

        for i, f_p in enumerate(folder_parting):
            fileList = []
            print(folder_[i],':',len(f_p))
            for fileN in f_p:
                if yolo:
                    shutil.copyfile(path + fileN + '.txt', output_path + folder_[i] +'/' + fileN +'.txt')
                else:    
                    run(classList, classNumList,path+fileN, output_path + folder_[i] +'/' + fileN +'.txt',labelGrep="")
                shutil.copyfile(path + fileN + '.jpg', output_path + folder_[i] +'/' + fileN +'.jpg')
                fileList.append(output_path + folder_[i] +'/' + fileN +'.jpg')

            with open(output_path + 'cfg/' + folder_[i] +'.txt', 'w') as the_file:
                for i in range(len(fileList)):
                    the_file.write(fileList[i] + "\n")

            the_file.close()

            if not yolo:
                print('bbox number:',classNumList,'\n')
                for i in classNumList:
                    classNumList[str(i)] = 0

        
        print(p,'transferYolo complete!')
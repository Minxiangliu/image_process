from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import darknet

import colors_array_80_class
from matplotlib import colors

FONT_SCALE = 0.8
FONT_THICKNESS = 1

Path = 'test_images/'

configPath = "cfg/yolov3.cfg"
weightPath = "yolov3.weights"
metaPath = "cfg/coco.data"

def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax

def matchColor(d):
    dict_detect = list(dict.fromkeys(d))
    for i, x in enumerate(dict_detect):
        d = [w.replace(x, colors_array_80_class.STANDARD_COLORS[i]) for w in d]
    return d

def cvDrawBoxes(detections, img):
    d = [x[0].decode() for x in detections]
    box_color_array = matchColor(d)
    i=0
    for detection in detections:
        c = colors.to_hex(box_color_array[i]).lstrip('#')
        drawColor = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        xmin, ymin, xmax, ymax = convertBack(
            float(x), float(y), float(w), float(h))
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        centerPoint = (xmin+int((xmax-xmin)/2),int(ymin+(ymax-ymin)/2))
        area = (xmax-xmin)*(ymax-ymin)

        (label_width, label_height), baseline = cv2.getTextSize(detection[0].decode(),
            cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, FONT_THICKNESS)

        cv2.rectangle(img, pt1, pt2, drawColor, 5)

        cv2.rectangle(img, 
            (pt1[0], pt1[1]-label_height-baseline),
            (pt1[0]+label_width, pt1[1]),
            drawColor, -1)

        cv2.putText(img,
            detection[0].decode(),
            (pt1[0], pt1[1]-baseline), cv2.FONT_HERSHEY_SIMPLEX, 
            FONT_SCALE,
            [0, 0, 0], FONT_THICKNESS)

        i += 1
    return img

netMain = None
metaMain = None
altNames = None

def YOLO(configPath, weightPath, metaPath):

    global metaMain, netMain, altNames
    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath)+"`")
    if netMain is None:
        netMain = darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    if metaMain is None:
        metaMain = darknet.load_meta(metaPath.encode("ascii"))
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(darknet.network_width(netMain),
                                    darknet.network_height(netMain),3)
    
    TEST_IMAGE_PATH = []
    files = os.listdir(Path)
    for f in files:
        if f.endswith('jpg'):
            TEST_IMAGE_PATH.append(Path+f)

    for i, im in enumerate(TEST_IMAGE_PATH):
        frame_read = cv2.imread(im)
        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb,
                                   (darknet.network_width(netMain),
                                    darknet.network_height(netMain)),
                                   interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())

        detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.5)

        image = cvDrawBoxes(detections, frame_resized)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite('outImage{}.jpg'.format(i), image)
        print('outImage{}.jpg'.format(i))

if __name__ == "__main__":
    YOLO(configPath, weightPath, metaPath)
    print('done!')

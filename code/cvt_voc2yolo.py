import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import glob
sets=['set_01','set_02','set_03','set_04','set_10','set_11','set_12']
classes = ["Knife","Bottle","Gun","Battery"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(set_name,anno_file_name):
    in_file = open('annotations/%s/%s.xml'%(set_name,anno_file_name))
    out_file = open('yolo_labels/%s/%s.txt'%(set_name,anno_file_name), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()
if not os.path.exists('yolo_labels'):
	os.makedirs('yolo_labels');
for set_name in sets:
    if not os.path.exists('yolo_labels/%s'%(set_name)):
        os.makedirs('yolo_labels/%s'%(set_name))
    anno_files = glob.glob('annotations/%s/*.xml'%(set_name))
    #list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for anno_file in anno_files:
    	anno_file_noext = anno_file.split('\\')[1].split('.')[0]
    	print set_name,' ',anno_file_noext
        convert_annotation(set_name,anno_file_noext)
        #list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))
    #list_file.close()


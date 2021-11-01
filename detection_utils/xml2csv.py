#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:    time:2021/11/1

import os
import glob
import pandas as pd
from tqdm import tqdm
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            bbx = member.find('bndbox')
            xmin = int(bbx.find('xmin').text)
            ymin = int(bbx.find('ymin').text)
            xmax = int(bbx.find('xmax').text)
            ymax = int(bbx.find('ymax').text)
            label = member.find('name').text

            value = (os.path.join('JPEGImages', root.find('filename').text),
                     xmin,
                     ymin,
                     xmax,
                     ymax,
                     label
                     )
            xml_list.append(value)
    xml_df = pd.DataFrame(xml_list)
    return xml_df


DATASET_PATH = '/home/zza/environments/AugmentedAutoencoder/detection_utils/output_det'

if __name__ == '__main__':
    annotaions_path = os.path.join(DATASET_PATH, 'Annotations')
    models_path = os.path.join(DATASET_PATH, 'models')
    models_files = glob.glob(os.path.join(models_path, '*.ply'))
    obj_ids = [int(file.split('_')[-1].split('.')[0]) for file in models_files]
    cls_list = []
    for obj_id in obj_ids:
        info = (obj_id, obj_id - 1)
        cls_list.append(info)
    cls_df = pd.DataFrame(cls_list)
    cls_df.to_csv(os.path.join(DATASET_PATH, 'classes.csv'),index=False, header=False)
    print('Successfully class mapping.')

    xml_df = xml_to_csv(annotaions_path)
    xml_df.to_csv(os.path.join(DATASET_PATH, 'annotations.csv'),index=False, header=False)
    print('Successfully converted xml to csv.')

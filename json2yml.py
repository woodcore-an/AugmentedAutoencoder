#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:    time:2021/10/29

import json
import ruamel.yaml as yaml

class ConvertJson2Yaml():
    def __init__(self, json_path, yml_path):
        self._json_path = json_path
        self._yml_path = yml_path

    def load_json(self, keys_to_int=True):
        def convert_keys_to_int(x):
            return {int(k) if k.lstrip('-').isdigit() else k: v for k, v in x.items()}

        with open(self._json_path, 'r') as f:
            if keys_to_int:
                contents = json.load(f, object_hook=lambda x: convert_keys_to_int(x))
            else:
                contents = json.load(f)

        return contents

    def save_info(self, info):
        for im_id in sorted(info.keys()):
            im_info = info[im_id]
            if 'cam_K' in im_info.keys():
                im_info['cam_K'] = im_info['cam_K']
            if 'cam_R_w2c' in im_info.keys():
                im_info['cam_R_w2c'] = im_info['cam_R_w2c']
            if 'cam_t_w2c' in im_info.keys():
                im_info['cam_t_w2c'] = im_info['cam_t_w2c']
        with open(self._yml_path, 'w') as f:
            yaml.safe_dump(info, f, encoding='utf-8', allow_unicode=True)

    def save_gt(self, gts):
        for im_id in sorted(gts.keys()):
            im_gts = gts[im_id]
            for gt in im_gts:
                if 'cam_R_m2c' in gt.keys():
                    gt['cam_R_m2c'] = gt['cam_R_m2c']
                if 'cam_t_m2c' in gt.keys():
                    gt['cam_t_m2c'] = gt['cam_t_m2c']
                if 'obj_bb' in gt.keys():
                    gt['obj_bb'] = [int(x) for x in gt['obj_bb']]
        with open(self._yml_path, 'w') as f:
            yaml.safe_dump(gts, f, encoding='utf-8', allow_unicode=True)




if __name__ == '__main__':
    json_file_path = "/home/zza/bop/convert/scene_camera.json"
    yml_file_path = "/home/zza/bop/convert/info.yml"

    # json_file_path = "/home/zza/bop/convert/scene_gt.json"
    # yml_file_path = "/home/zza/bop/convert/gt.yml"

    c = ConvertJson2Yaml(json_file_path, yml_file_path)
    content = c.load_json()
    c.save_info(content)
    # c.save_gt(content)



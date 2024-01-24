# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime


def set_common():
    with open('./conf/common.json', 'r') as f:
        common_conf = json.load(f)

    return common_conf


def set_log():
    if not os.path.isdir('./log/'):
        os.mkdir('./log/')

    with open('./conf/log.json', 'r') as f:
        log_conf = json.load(f)
    log_conf["handlers"]["fileHandler"]["filename"] = './log/{}.log'.format(datetime.utcnow().strftime("%Y%m%d%H%M%S"))

    return log_conf


def input_text(filename):
    with open("./text/input/{}".format(filename), encoding='utf-8') as f:
        text = f.read()
    return text


def output_text(filename, result_dict):
    summarize_results = result_dict['summarize_result']
    with open("./text/output/【要約】{}".format(filename), mode='w', encoding='utf-8') as f:
        for result in summarize_results:
            f.writelines(result)

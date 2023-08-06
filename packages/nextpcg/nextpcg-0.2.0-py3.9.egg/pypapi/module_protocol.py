# -*- coding: utf-8 -*-
"""simple protocol for dispatch to user defined module
Author  : NextPCG
"""

import os
import json

PROTOCOL_DONE = "s8xc32ds5f" # abitray code


def module_send_done():
    print(PROTOCOL_DONE)


def server_check_done(proc, logger):
    """check whether task is done
    
    Args:
        proc(subprocess.Popen): process running dson_main.py """
    a = proc.stdout.readline()
    while not PROTOCOL_DONE in a:
        if not a:
            # check if proc is dead
            if proc.poll() is not None:
                # proc is terminated
                raise ProcessLookupError("subprocess is terminated by unknown bug")
        logger.info(a)
        a = proc.stdout.readline()


def server_send_dson(dson_data, work_path, proc):
    json_data_temp_name = os.path.join(work_path, "temp.json").replace('\\','/')
    if not os.path.exists(work_path):
        os.makedirs(work_path, exist_ok=True)
    with open(json_data_temp_name, "w", encoding="utf-8") as f:
        json.dump(dson_data, f)
    proc.stdin.write(json_data_temp_name + " " + work_path + "\n")
    proc.stdin.flush()

def server_load_dson(work_path):
    dson_error_data = {}
    json_data_temp_name = os.path.join(work_path, "temp.json").replace('\\','/')
    with open(json_data_temp_name, "r", encoding='utf-8') as f:
        dson_data = json.load(f)
    json_error_data_name = os.path.join(work_path, 'error.json').replace('\\','/')
    if os.path.exists(json_error_data_name):
        with open(json_error_data_name, 'r', encoding='utf-8') as f:
            dson_error_data = json.load(f)
    return dson_data, dson_error_data
    
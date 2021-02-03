#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/2/1 14:50
# @Author  : ningbo
# @File    : redfish.py
# @Software: python2.7

import argparse
import json
import os
import sys
import time
from pprint import pprint

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

basepath = "/home/nfs/fw"
head = {
    "Authorization": "Basic QWRtaW5pc3RyYXRvcjpBZG1pbkA5MDAw",
}
NFS_IP = "192.168.16.1"


def log(msg, is_print=True):
    log_path = "log.txt"
    if is_print == True:
        print msg
    with open(log_path, "a") as f:
        f.write(msg)
        f.write("\n")


def query_task(ip, fw, id):
    try:
        r = requests.get("https://{}/redfish/v1/TaskService/Tasks/{}".format(ip, id), headers=head, verify=False)
    except Exception:
        log("网络故障，或该IP的机器未查询到！")
        sys.exit()
    r_json = r.json()
    d = {}
    d["Messages"] = r_json["Messages"].get("Message")
    d["TaskState"] = r_json.get("TaskState")
    try:
        if d["TaskState"] == "Running":
            log(d["Messages"])
            time.sleep(5)
            query_task(ip, fw, id)
        elif d["TaskState"] == "Completed":
            raise Exception("完成标志")
        else:
            log("更新{}固件失败！".format(fw))
            log(d["Messages"])
            sys.exit()
    except Exception:
        log("更新{}固件成功！".format(fw))
        return


def fw_up(fw_path, ip):
    data_up = {
        "ImageURI": "nfs://{}:{}".format(NFS_IP, fw_path),
        "TransferProtocol": "NFS",
    }
    try:
        r = requests.post("https://{}/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate".format(ip),
                          headers=head,
                          json=data_up, verify=False)
    except Exception:
        log("网络故障，或该IP的机器未查询到！")
        sys.exit()
    r_json = r.json()
    d = {}
    d.setdefault("Messages", None)
    d["Messages"] = r_json["Messages"]  # 消息列表
    d["TaskState"] = r_json.get("TaskState")
    d["Id"] = r_json["Id"]
    if d["TaskState"] == "Running":
        return fw, d["Id"]
    else:
        log("更新{}固件失败！".format(fw))
        pprint(d["Messages"])
        log(json.dumps(d["Messages"]), is_print=False)
        sys.exit()


def systemOverview(ip):
    log("正在查询ip:{}的固件版本信息......".format(ip))
    try:
        r = requests.get("https://{}/redfish/v1/SystemOverview".format(ip), headers=head, verify=False)
    except Exception:
        log("网络故障，或该IP的机器未查询到！")
        sys.exit()
    r_json = r.json()
    d = {}
    d["ProductName"] = r_json["Systems"][0].get("ProductName") + " (" + r_json["Systems"][0].get(
        "ProductAlias") + ")"
    d["BiosVersion"] = r_json["Systems"][0].get("BiosVersion")
    d["FirmwareVersion"] = r_json["Managers"][0].get("FirmwareVersion")
    d["SystemSerialNumber"] = r_json["Systems"][0].get("SystemSerialNumber")
    d["PermanentMACAddress"] = r_json["Managers"][0].get("PermanentMACAddress")
    pprint(d)
    log(json.dumps(d), is_print=False)
    return d


def file_list(fw_dir):
    path = os.path.join(basepath, fw_dir)
    l = [i for i in os.listdir(path) if i.endswith(".hpm")]
    l.sort()
    return l


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="鲲鹏服务器更新固件")
    parser.add_argument("-i", type=str, required=True, help="请输入测试机的ip：")
    parser.add_argument("-f", type=str, default="", help="更新固件的文件夹名字。")
    parser.add_argument("-q", action="store_true", default=False, help="查询测试机的固件版本信息。")
    args = parser.parse_args()
    if args.q == True:
        systemOverview(args.i)
    elif len(args.f) > 0:
        fw_list = file_list(args.f)
        for fw in fw_list:
            log("ip:{}正在更新固件{}中......".format(args.i, fw))
            fw_path = os.path.join(basepath, args.f, fw)
            r_fw, r_id = fw_up(fw_path, args.i)
            time.sleep(3)
            query_task(args.i, r_fw, r_id)
    else:
        log("参数组合不正确，或缺少参数！")

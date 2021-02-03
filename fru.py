# coding=UTF-8

import json, subprocess, re, sys


class SN():
    def __init__(self, ip=None):
        self.command_map = {
            "Chassis Part Number": (" raw 0x0a 0x12 0x00 0x0c 0x00 ", 23),  # 23
            "Chassis Serial": (" raw 0x0a 0x12 0x00 0x24 0x00 ", 23),  # 23
            "Board Mfg": (" raw 0x0a 0x12 0x00 0x47 0x00 ", 7),  # 7
            "Board Product": (" raw 0x0a 0x12 0x00 0x4f 0x00 ", 17),  # 17
            "Board Serial": (" raw 0x0a 0x12 0x00 0x61 0x00 ", 23),  # 23
            "Board Part Number": (" raw 0x0a 0x12 0x00 0x79 0x00 ", 23),  # 23
            "Product Manufacturer": (" raw 0x0a 0x12 0x00 0x9c 0x00 ", 7),  # 7
            "Product Name": (" raw 0x0a 0x12 0x00 0xa4 0x00 ", 17),  # 17
            "Product Part Number": (" raw 0x0a 0x12 0x00 0xb6 0x00 ", 23),  # 23
            "Product Version": (" raw 0x0a 0x12 0x00 0xce 0x00 ", 4),  # 4
            "Product Serial": (" raw 0x0a 0x12 0x00 0xd3 0x00 ", 23),  # 23
            "Product AssetTag": (" raw 0x0a 0x12 0x00 0xeb 0x00 ", 16),  # 16
        }
        self.ip = ip
        self.args = {}
        self.head = ""

    def run(self, bs, cs, ps):
        flag = True
        self.args_load()
        self.args["dmi"]["Board Serial"] = bs
        self.args["dmi"]["Chassis Serial"] = cs
        self.args["dmi"]["Product Serial"] = ps
        for k, v in self.args["dmi"].items():
            flag &= self.fru_key_write(k, v)
        if flag:
            print("写入成功\n")
        else:
            print("写入失败\n")

    def args_load(self, file="args.json"):
        try:
            with open(file, "r") as f:
                self.args = json.load(f)
            self.head = "ipmitool.exe -I lanplus -H {} -U {} -P {}" \
                .format(self.ip, self.args["user"], self.args["password"])
        except(FileNotFoundError):
            sys.exit("{}文件不存在".format(file))

    def fru_key_write(self, key, value):
        l = []
        if len(value) > self.command_map[key][1]:
            print("{}:{}\t写入字段长度超过限制,长度应不超过{}!".format(key, value, self.command_map[key][1]))
            return False
        valueSpace = value + " " * (self.command_map[key][1] - len(value))
        for i in valueSpace:
            l.append(hex(ord(i)))
        hexstring = " ".join(l)
        cmd = self.head + self.command_map[key][0] + hexstring
        status, _ = subprocess.getstatusoutput(cmd)
        if status != 0:
            print("{}:{}\t写入失败!".format(key, value))
            return False
        return True

    @staticmethod
    def getDataFromFile(file="sn.txt"):
        try:
            with open(file, "r") as f:
                data = f.read()
            l = re.findall(r"(\w+)[ ]+(\w+)[ ]+(\w+)[ ]+(\w+)[ ]+(\w+)[ ]+(\w+)", data)
            d = {}
            for uut in l:
                d[uut[3].upper()] = (uut[0], uut[4], uut[5])
            return d
        except(FileNotFoundError):
            sys.exit("{}文件不存在".format(file))

    @staticmethod
    def getIpFromMac():
        status, out = subprocess.getstatusoutput("arp -a")
        if status != 0:
            sys.exit("error,请使用windows7及以上系统!")
        l = re.findall(r"([\d.]+)[ ]+([\w-]+[\w]+)[ ]+", out)
        d = {}
        for i in l:
            d[i[1].replace("-", "").upper()] = i[0]
        return d


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(["[指定ip写入模式]"])# 指定ip写入模式
        ip = sys.argv[1]
        print("正在写入{}机器的fru信息......".format(ip))
        bs = input("Board Serial：").strip()
        cs = input("Chassis Serial：").strip()
        ps = input("Product Serial：").strip()
        obj = SN(ip)
        obj.run(bs, cs, ps)
    else:  # sn文件读取自动写入模式
        print("[自动写入模式]")
        macs_from_LAN = SN.getIpFromMac()
        macs_from_file = SN.getDataFromFile()
        for mac, ip in macs_from_LAN.items():
            bs_ps_cs = macs_from_file.get(mac)
            if bs_ps_cs != None:
                print("正在写入{}:{}机器的fru信息......".format(ip, mac))
                bs, ps, cs = bs_ps_cs
                obj = SN(ip)
                obj.run(bs, cs, ps)
        sys.exit("局域网中的所有机器已写入完毕")

    # for uut in SN.getDataFromFile():
    #     mac = uut[3].upper()
    #     print("正在写入机器bmcMAC地址为{}的fru信息......".format(mac))
    #     ip = SN.getIpFromMac(mac)
    #     if ip != None:
    #         bs = uut[0]
    #         ps = uut[4]
    #         cs = uut[5]
    #         obj = SN(ip)
    #         obj.run(bs, cs, ps)
    #     else:
    #         print("从区域网中获取MAC地址为{}的ip不存在".format(mac))
    #         ip = input("请手动输入机器bmcMAC地址为{}的ip：".format(mac)).strip()
    #         bs = uut[0]
    #         ps = uut[4]
    #         cs = uut[5]
    #         obj = SN(ip)
    #         obj.run(bs, cs, ps)

# coding:utf-8

import requests
import paramiko
import threading
import time
import json

EXEC_FILE = "exec.json"
UPLOAD_FILE = "upload.json"
DOWNLOAD_FILE = "download.json"
COMBINED_FILE = "conbined.json"
banner = """
    ___        ______        _____
   / \ \      / /  _ \      |  ___| __ __ _ _ __ ___   ___
  / _ \ \ /\ / /| | | |_____| |_ | '__/ _` | '_ ` _ \ / _ \\
 / ___ \ V  V / | |_| |_____|  _|| | | (_| | | | | | |  __/
/_/   \_\_/\_/  |____/      |_|  |_|  \__,_|_| |_| |_|\___|    
                                                               
"""


def ssh(ip, username, passwd, cmd):  # 批量修改ssh密码/执行命令
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd, timeout=5)

        stdin, stdout, stderr = ssh.exec_command(cmd)
        #           stdin.write("Y")   #简单交互，输入 ‘Y’
        out = stdout.readlines()

        print "[stdin:]"
        print cmd
        # 屏幕输出
        print "[stdout:]"
        for o in out:
            print o,
        err = stderr.readlines()
        # 屏幕输出
        print "[stderr:]"
        for o in err:
            print o,
        ssh.close()
    except:
        print '[%s\tError]\n' % (ip)


def read_json(file_name):
    with open(file_name, 'r') as load_f:
        load_dict = json.load(load_f)
        print "[load file]"
        return load_dict


def write_json(file_name, load_dict):
    with open(file_name, "w") as dump_f:
        print "[write json:]"
        print(load_dict)
        json.dump(load_dict, dump_f)


def ssh_execmd_by_host(load_dict):  # 调用ssh函数执行命令
    for host in load_dict:
        print "[host info:]"
        print host
        ip = host["ip"]
        username = host["username"]
        passwd = host["passwd"]
        cmds = host["cmds"]
        for cmd in cmds:
            ssh(ip, username=username, passwd=passwd, cmd=cmd)  # 单个IP的情况
        print '[%s\texec complete]\n' % (ip)


def upload_file(ip, username, passwd, remotepath, localpath):
    t = paramiko.Transport((ip, 22))
    t.connect(username=username, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(localpath, remotepath)
    t.close()


def download_file(ip, username, passwd, remotepath, localpath):
    t = paramiko.Transport((ip, 22))
    t.connect(username=username, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(remotepath, localpath)
    t.close()


def ssh_upload_by_host(load_dict):  # 调用ssh函数执行命令
    for host in load_dict:
        print "[host info:]"
        print host
        ip = host["ip"]
        username = host["username"]
        passwd = host["passwd"]
        filelist = host["filelist"]
        for f in filelist:
            upload_file(ip, username=username, passwd=passwd, remotepath=f["remotepath"],
                        localpath=f["localpath"])  # 单个IP的情况
        print '[%s\tupload complete]\n' % (ip)


def ssh_download_by_host(load_dict):  # 调用ssh函数执行命令
    for host in load_dict:
        print "[host info:]"
        print host
        ip = host["ip"]
        username = host["username"]
        passwd = host["passwd"]
        filelist = host["filelist"]
        for f in filelist:
            download_file(ip, username=username, passwd=passwd, remotepath=f["remotepath"],
                          localpath=f["localpath"])  # 单个IP的情况
        print '[%s\tdownload complete]\n' % (ip)


token = ""


def submit_flag(flag, token):
    burp0_url = "http://month.ctf.huawei.com:80/sendconflictflag"
    burp0_cookies = {"_dmpa_id": "76367b2f1d8fe8b7d4d4c300751671490871593870.1490871594.22.1537176057.1536407795.",
                     "_dmpa_ref": "%5B%22%22%2C%22%22%2C1537010965%2C%22http%3A%2F%2Fwww.honor.cn%2F%22%5D",
                     "v1st": "15B1EE2C0AD355FF",
                     "FORUM_LOGIN_AUTH_SECURE_CODE": "77-43-D3-93-27-3F-2E-44-76-F7-5E-A6-81-20-9E-CD-9F-83-79-3C-BF-1F-59-D4-E6-33-0E-6A-3D-67-33-92-40-FF-7B-F8-07-F7-24-0B-00-88-F4-AA-7D-8E-6C-D1-BD-B0-89-4D-C4-54-80-37",
                     "__hau": "HuaweiConnect.1515720684.50520363",
                     "AMCV_7DA25C0158C1322D0A495DB1%40AdobeOrg": "1099438348%7CMCIDTS%7C17569%7CMCMID%7C45641806404925707266212307174569030497%7CMCAID%7CNONE%7CMCOPTOUT-1517917697s%7CNONE%7CvVersion%7C2.1.0",
                     "support_last_vist": "carrier", "HW3MS_think_language": "zh-cn", "authmethod": "authpwd",
                     "hwssot3": "26275226252217", "hwsso_login": "\"\"",
                     "_dmpa_ses": "f2caad30c2e98637cd16e442f83241e0a9ff89dc",
                     "HWFORUM_SESSION": "0f3f5d5d24336b92b6c81e752f4b62e760e8d7a11a7f395d00932445d90c3d2a0901608421bbf58382f5dc89c7e129a4ae44c365752abe426086200d5d1c8e98f462a18c8404e2f3697388af71454172",
                     "MacaronSession": "0025d0221b7fc983"}
    burp0_headers = {"POST http": "/month.ctf.huawei.com/sendconflictflag HTTP/1.1",
                     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0",
                     "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                     "Accept-Encoding": "gzip, deflate", "Referer": "http://month.ctf.huawei.com/conflict",
                     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     "X-Requested-With": "XMLHttpRequest", "DNT": "1", "Connection": "close"}
    burp0_data = {"flag": flag}
    print "[+] Submiting flag : [%s]" % (burp0_data)
    r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data).content
    content = str(r)
    print "[+] Content : %s" % (content)


def exp():
    with open("flag", 'r') as file:
        while 1:
            line = file.readline()
            if not line:
                break
            flag = line.strip()
            submit_flag(flag=flag, token="")


if __name__ == '__main__':
    print banner
    load_dict = read_json(COMBINED_FILE)
    while True:
        for action in load_dict:
            if action["type"] == "exec":
                ssh_execmd_by_host(action["content"])
            elif action["type"] == "upload":
                ssh_upload_by_host(action["content"])
            elif action["type"] == "download":
                ssh_download_by_host(action["content"])
            else:
                continue
        exp()
        time.sleep(60)

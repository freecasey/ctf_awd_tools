# coding:utf-8
import threading

import paramiko
import time
import json
import datetime

EXEC_FILE = "exec.json"
UPLOAD_FILE = "upload.json"
DOWNLOAD_FILE = "download.json"
COMBINED_FILE = "tcpdump_mul.json"
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

        print "[stdin:]"
        print cmd
        stdin, stdout, stderr = ssh.exec_command(command=cmd, timeout=60)
        #           stdin.write("Y")   #简单交互，输入 ‘Y’
        out = stdout.readlines()

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
        print '[%s\t exec Error]\n' % (ip)
        ssh.close()


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
    host = load_dict[0]
    print "[exec host info:]"
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


def mkdir(path):
    import os
    if not os.path.exists("tcpdump"):
        os.makedirs("tcpdump")
    path = "tcpdump//" + path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        print "[make dir:" + path + "]"
        os.makedirs(path)
    return


def ssh_upload_by_host(load_dict):  # 调用ssh函数执行命令
    host = load_dict[0]
    print "[upload host info:]"
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
    host = load_dict[0]
    print "[download host info:]"
    print host
    ip = host["ip"]
    username = host["username"]
    passwd = host["passwd"]
    filelist = host["filelist"]
    mkdir(ip)
    for f in filelist:
        prefix = "tcpdump//" + ip + "//"
        suffix = "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".pcap"
        download_file(ip, username=username, passwd=passwd, remotepath=f["remotepath"],
                      localpath=prefix + f["localpath"] + suffix)  # 单个IP的情况
    print '[%s\tdownload complete]\n' % (ip)

def down_clr(exec_cmd, clr, download, upload):
    while True:
        # time.sleep(60)
        ssh_execmd_by_host(exec_cmd)
        ssh_execmd_by_host(clr)
        ssh_download_by_host(download)



def exp():

    load_dict = read_json(COMBINED_FILE)
    for item in load_dict:
        download = None
        clr = None
        upload = None
        exec_cmd = None
        for action in item['host']:

            if action["type"] == "exec":
                exec_cmd = action["content"]
            elif action["type"] == "upload":
                upload = action["content"]
            elif action["type"] == "download":
                download = action["content"]
            elif action["type"] == "clear":
                clr = action["content"]
            else:
                continue
        # threading.Thread(target=ssh_execmd_by_host, args=(exec_cmd,)).start()
        threading.Thread(target=down_clr, args=(exec_cmd, clr, download, upload)).start()


if __name__ == '__main__':
    print banner
    # load_dict = read_json(UPLOAD_FILE)
    # ssh_upload_by_host(load_dict)
    # load_dict = read_json(EXEC_FILE)
    # ssh_execmd_by_host(load_dict)
    # load_dict = read_json(DOWNLOAD_FILE)
    # ssh_download_by_host(load_dict)
    exp()

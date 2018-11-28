#coding:utf-8

import requests
import paramiko
import threading
import  time
import json

EXEC_FILE="exec.json"
UPLOAD_FILE="upload.json"
DOWNLOAD_FILE="download.json"
COMBINED_FILE = "modify_passwd.json"
banner = """
    ___        ______        _____
   / \ \      / /  _ \      |  ___| __ __ _ _ __ ___   ___
  / _ \ \ /\ / /| | | |_____| |_ | '__/ _` | '_ ` _ \ / _ \\
 / ___ \ V  V / | |_| |_____|  _|| | | (_| | | | | | |  __/
/_/   \_\_/\_/  |____/      |_|  |_|  \__,_|_| |_| |_|\___|    
                                                               
"""
def ssh(ip,username,passwd,cmd):  #批量修改ssh密码/执行命令
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)

        stdin, stdout, stderr = ssh.exec_command(cmd)
#           stdin.write("Y")   #简单交互，输入 ‘Y’
        out = stdout.readlines()

        print "[stdin:]"
        print cmd
        #屏幕输出
        print "[stdout:]"
        for o in out:
            print o,
        err = stderr.readlines()
        # 屏幕输出
        print "[stderr:]"
        for o in err:
            print o,
        ssh.close()
    except :
        print '[%s\tError]\n'%(ip)

def read_json(file_name):
    with open(file_name, 'r') as load_f:
        load_dict = json.load(load_f)
        print "[load file]"
        return load_dict

def  write_json(file_name, load_dict):
    with open(file_name, "w") as dump_f:
        print "[write json:]"
        print(load_dict)
        json.dump(load_dict, dump_f)

def ssh_execmd_by_host(load_dict): # 调用ssh函数执行命令
    for host in load_dict:
        print "[exec host info:]"
        print host
        ip = host["ip"]
        username = host["username"]
        passwd =  host["passwd"]
        cmds =  host["cmds"]
        for cmd in cmds:
            ssh(ip,username=username,passwd=passwd,cmd=cmd) # 单个IP的情况
        print '[%s\texec complete]\n'%(ip)

def upload_file(ip,username,passwd,remotepath, localpath):
    t = paramiko.Transport((ip, 22))
    t.connect(username = username, password = passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(localpath,remotepath)
    t.close()

def download_file(ip,username,passwd,remotepath, localpath):
    t = paramiko.Transport((ip, 22))
    t.connect(username = username, password = passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(remotepath, localpath)
    t.close()

def ssh_upload_by_host(load_dict): # 调用ssh函数执行命令
    for host in load_dict:
        print "[upload host info:]"
        print host
        ip = host["ip"]
        username = host["username"]
        passwd =  host["passwd"]
        filelist =  host["filelist"]
        for f in filelist:
            upload_file(ip,username=username,passwd=passwd,remotepath=f["remotepath"], localpath=f["localpath"]) # 单个IP的情况
        print '[%s\tupload complete]\n'%(ip)

def ssh_download_by_host(load_dict): # 调用ssh函数执行命令
    for host in load_dict:
        print "[download host info:]"
        print host
        ip = host["ip"]
        username = host["username"]
        passwd =  host["passwd"]
        filelist =  host["filelist"]
        for f in filelist:
            download_file(ip,username=username,passwd=passwd,remotepath=f["remotepath"], localpath=f["localpath"]) # 单个IP的情况
        print '[%s\tdownload complete]\n'%(ip)

def exp():
    load_dict = read_json(COMBINED_FILE)
    for action in load_dict:
        if action["type"] == "exec":
            ssh_execmd_by_host(action["content"])
        elif action["type"] == "upload":
            ssh_upload_by_host(action["content"])
        elif action["type"] == "download":
            ssh_download_by_host(action["content"])
        else:
            continue

if __name__=='__main__':
    print banner
    # load_dict = read_json(UPLOAD_FILE)
    # ssh_upload_by_host(load_dict)
    # load_dict = read_json(EXEC_FILE)
    # ssh_execmd_by_host(load_dict)
    # load_dict = read_json(DOWNLOAD_FILE)
    # ssh_download_by_host(load_dict)
    exp()

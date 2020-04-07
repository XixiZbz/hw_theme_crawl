#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/23 5:26 下午
# @Author  : zbz
# @Site    :
# @File    : loader.py
# @Software: PyCharm


import sys
import os
import threading
import subprocess
import time

import frida

jscode = """ 
Java.perform(function () { 
    var d = Java.use('okhttp3.internal.g.d'); 
    try { 
         d.verify.overload('java.lang.String', 'javax.net.ssl.SSLSession').implementation = function(p0, p1){ 
             console.log('ssl unpinning for "' + p0 + '"'); 
             return true; 
       }; 
     } catch (e) { 
        console.log(e); 
    }        
}); 
"""


def start_frida_server():
    """启动Frida服务端
    """
    # 判断/data/local/tmp/frida是否存在
    # cmd_ret = subprocess.check_output('adb shell ls /data/local/tmp/frida', shell=True)
    os.system('adb forward tcp:27042 tcp:27042')
    os.system('adb forward tcp:27043 tcp:27043')


if __name__ == '__main__':
    # 启动模拟器内的Frida server
    start_frida_server()

    # 启动目标APP，并注入hook代码
    # APP_NAME = ['com.bbk.theme']
    device = frida.get_usb_device()
    # 启动`demo02`这个app
    pid = device.spawn(["com.bbk.theme"])
    device.resume(pid)
    time.sleep(1)
    session = device.attach(pid)
    # 加载s1.js脚本
    with open("frida_test.js") as f:
        script = session.create_script(f.read())
    script.load()

    sys.stdin.read()
    # 脚本会持续运行等待输入
    # raw_input()
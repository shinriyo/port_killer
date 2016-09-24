#!/Users/shinriyo/fushicho_py/env/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import socket
# import subprocess
import re

def check_port(port_num):
    """
    ポートを調べる
    :return: ポートが使われてなければTrueで使われてたらFalse
    """
    # print('check_port')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port_num))

    if result == 0:
        # print("ポート %d は使用しています。" % port_num)
        print("The port %d is using." % port_num)
        return False
    else:
        # print("ポート %d は使用していません。" % port_num)
        sys.exit("The port %d is not used." % port_num)
        return True # ここは通らないけど

LINUX = 0
MAC = 1
WINDOWS = 2
OTHER = 3

def get_os():
    from sys import platform as _platform
    if _platform in ["linux", "linux2"]:
        return LINUX
    elif _platform == "darwin":
        return MAC
    elif _platform == "win32":
        return WINDOWS
    else:
        return OTHER

def get_killable_process(port_num):
    """
    ポートに対して殺せるプロセス番号を得る
    :param port_num:
    :return: プロセスの番号、なければ空文字
    """
    txt_file_name = "net.txt"
    # Linux
    if get_os() == LINUX:
        os.system("netstat -anp | grep %d > %s" % (port_num, txt_file_name))
    # Mac OS
    elif get_os() == MAC:
        os.system("lsof -n -P -i :%d | grep %d > %s" % (port_num, port_num, txt_file_name))
    # Windows
    elif get_os() == WINDOWS:
        sys.exit('Windows OS is not supported.')
    else:
        sys.exit('unknown OS is not supported.')

    f = open(txt_file_name, "r")
    # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    lines = f.readlines()
    f.close()

    killable_process = ''

    for line in lines:
        # 犯人
        # Linux
        # res = re.search('(\d+)(?=/.*)', line)
        # Mac
        # python  25462 shinriyo    5u  IPv4 0x69c76ff36ff53e9b      0t0  TCP *:5000 (LISTEN)
        res = re.search('(\d+)', line)
        # 正規表現に引っかからなかったらNoneなのでそれを弾く
        if res != None:
            # net.txt削除
            # f = open(txt_file_name, "r")
            print res.group()
            killable_process = res.group()
            print 'killable process: %s' % killable_process

    return killable_process

if __name__ == "__main__":
    argvs = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argvs) # 引数の個数
    port_num = 8080

    # 引数が1つなのは自分自身の.py
    if (argc == 1):
        pass
    elif (argc == 2):
        arg_port = argvs[1]
        # 整数の時だけ
        try:
            int(arg_port, 10)
        except:
            sys.exit('Port number is not number.')
        else: # success
            port_num = int(arg_port)
    else:
        sys.exit('Argments are invalid.')

    # ポート名をセット
    # ポートが-1でなくなおかつファイルが存在するかをチェックする
    if port_num != -1 and True:
        if check_port(port_num):
           # 使っているportでのプロセスはないです。
            sys.exit('The process of the port number does not exist.')
        else:
            # killすべきプロセス
            killable_process = get_killable_process(port_num)
            if killable_process != '':
                # name = raw_input('プロセス%sをkillしますか？ [y/n]' % killable_process)
                name = raw_input('Do you kill the process %s? [y/n]' % killable_process)
                if name == 'y':
                    os.kill(int(killable_process), 9)
                else:
                    print 'Successly stopped'
                    sys.exit()
            else:
                # Processをkillできなかった
                sys.exit('can\'t killed the process.')
    else:
        # 実行出来ませんでした。
        sys.exit('Killing process failed.')


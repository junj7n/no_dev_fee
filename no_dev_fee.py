#!/usr/bin/env python
#-*-encoding:UTF-8-*-

# This is Bitcoin_No_Dev_Fee_Tool, support all use stratum protocol miner, such as eth, etc, zec, sc.
# 
# We use pydivert (https://pypi.python.org/pypi/pydivert/2.0.1) capture and inject miner network packet 
# with user bitcoin address replacing dev address.
# 
# usage: python python no_dev_fee.py {coin_adress} {stratum_port}
# eg: python no_dev_fee.py t1T3Q9rdqR8jWk4g7yaWoDKa2dcyG8QLcgU 3329
#
# package exe: pip install pyinstaller
# pyinstaller no_dev_fee.py -F -i logo.ico
#=============================================================================
# !Notice before package, we must modify C:\Python27\Lib\site-packages\pydivert\windivert_dll\__init__.py 35 line
# In this way, we can load WinDivert64.dll in current path avoid pyinstaller dll bug.
#
# if platform.architecture()[0] == "64bit":
#     #DLL_PATH = os.path.join(here, "WinDivert64.dll")
#     DLL_PATH = "WinDivert64.dll"
# else:
#     #DLL_PATH = os.path.join(here, "WinDivert32.dll")
#     DLL_PATH = "WinDivert32.dll"
#=============================================================================

import pydivert
import json
import sys
import os

if len(sys.argv) < 3:
    print("Administrator privileges must be need")
    print("usage: python no_dev_fee.py {coin_address} {stratum_port}")
    print("eg: python no_dev_fee.py t1T3Q9rdqR8jWk4g7yaWoDKa2dcyG8QLcgU 3329")
    os.system("pause")
    exit(0)

address = sys.argv[1]
port = sys.argv[2]

print('start to watch mining networking port...')
print('replace dev address to => %s by watching port => %s' % (address, port))

with pydivert.WinDivert("tcp.DstPort == %s and tcp.PayloadLength > 0" % port ) as w:
    for packet in w:
        if packet == None or packet.tcp == None or packet.tcp.payload == None:
            w.send(packet)
            continue
        print(packet.tcp.payload)


        # 1) zec stratum protocol  method: mining.authorize/mining.submit contains wallet address
        # doc https://github.com/ctubio/php-proxy-stratum/wiki/Stratum-Mining-Protocol
        # 2) eth stratum protocol  method: eth_submitLogin contains wallet address
        # 3) etc stratum protocol  method: eth_submitLogin
        # Please watch claymore log file, eth and etc modify stratum protocol

        payload = packet.tcp.payload
        if payload.find(address) < 0:
            if payload.find('mining.submit') > 0 or payload.find('mining.authorize') > 0 or payload.find('eth_submitLogin') > 0:
                print('find dev address ok!')
                json_data = json.loads(payload)
                if json_data['params'] and len(json_data['params']) > 0:
                    originAddr = json_data['params'][0]
                    newParam = address
                    if originAddr.find('.') > 0:
                        newParam = address + originAddr[originAddr.find('.'):]
                    json_data['params'][0] = newParam

                print('replace with new address => ' + newParam)
                payload = json.dumps(json_data)

     	# inject data, and send packat
        packet.tcp.payload = payload
        w.send(packet)

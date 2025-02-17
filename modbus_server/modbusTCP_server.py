#*******************************************************************
#                       MODBUS TCP - SERVER
#*******************************************************************
'''
File name: modbusTCP_server.py
Description: This program implements a minimal code to create a
             modbus TCP server.
URL to Download:
    https://github.com/LeandroTeodoroRJ/ModbusTCP-IP
Stable: Yes
Version: 2.0.0
Current: Yes
Maintainer: leandroteodoro.engenharia@hotmail.com
Depends:
    pyModbusTCP==0.3.0
Architecture: X86
Compile/Interpreter: python 3.1.12
Access: Public
Changelog: No changelog
Readme: No readme (inside this code)
Document Extra-Files:
    server_modbusTCP.log    Arquivo de Logs do sistema
Links:
    pyModbus Documentation - https://pypi.org/project/pyModbusTCP/
Other Notes:
    * Run this as root to listen on TCP privileged ports (<= 1024).
    * To run
        Add "--host 0.0.0.0" to listen on all available IPv4 addresses of the host.
        sudo <full interpreter path> ./modbusTCP_server.py --host 0.0.0.0
        sudo /home/leandro/Dev/py3-10_modbusTCP/bin/python3 ./modbusTCP_server.py --host 0.0.0.0 --debug&
'''

#!/usr/bin

import argparse
import logging

from pyModbusTCP.server import ModbusServer

# init logging
logging.basicConfig(
    format="%(asctime)s, %(levelname)s, %(message)s",
    filename="server_modbusTCP.log")
# parse args
parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host', type=str, default='localhost', help='Host (default: localhost)')
parser.add_argument('-p', '--port', type=int, default=502, help='TCP port (default: 502)')
parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
args = parser.parse_args()
# logging setup
if args.debug:
    logging.getLogger('pyModbusTCP.server').setLevel(logging.DEBUG)
# start modbus server
server = ModbusServer(host=args.host, port=args.port)
server.start()

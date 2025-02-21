#*******************************************************************
#                    MODBUS TCP - CLIENT POLLING
#*******************************************************************
'''
File name: modbusTCP_polling.py
Description: This program implements a Modbus TCP client running as polling.
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
    No Extra Files.
Links:
    pyModbus Documentation - https://pypi.org/project/pyModbusTCP/
Other Notes:
    * Run this as root to listen on TCP privileged ports (<= 1024).
    * To run
        sudo <full interpreter path> ./modbusTCP_service.py
        sudo /home/leandro/Dev/py3-10_modbusTCP/bin/python3 ./modbusTCP_polling.py
'''

import time

from pyModbusTCP.client import ModbusClient

SERVER_HOST = "192.168.1.2"
SERVER_PORT = 502

# TCP auto connect on modbus request
tcp_comm = ModbusClient(host=SERVER_HOST, auto_open=True, unit_id=1, port=SERVER_PORT)

#Start service
while True:
    #Read discrete inputs
    #Modbus funtion 0x02
    read_coils = tcp_comm.read_discrete_inputs(0, 10)
    fail = None
    if read_coils != fail:
        print('input status ad #0 to 9: %s' % read_coils)
    else:
        print('unable to read discrete inputs')

    #Read input registers 2x 16 bits registers at modbus address 0
    #Modbus funtion 0x04
    regs = tcp_comm.read_input_registers(0, 2)
    fail = None
    if regs != fail:
        print("input registers: %s" %regs)
    else:
        print("read error")

    print("")
    # 1s before to next loop
    time.sleep(1)

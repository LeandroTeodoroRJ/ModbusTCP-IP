#*******************************************************************
#                       MODBUS TCP - CLIENT
#*******************************************************************
'''
File name: modbusTCP_client.py
Description: This program implements a minimal code to create a
             modbus TCP client.
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
        sudo <full interpreter path> ./modbusTCP_client.py
        sudo /home/leandro/Dev/py3-10_modbusTCP/bin/python3 ./modbusTCP_client.py
'''

from pyModbusTCP.client import ModbusClient

# TCP auto connect on modbus request, close after it
tcp_comm = ModbusClient(host="192.168.1.2", auto_open=True, unit_id=1, auto_close=True)

#Read holding registers 2x 16 bits registers at modbus address 0
regs = tcp_comm.read_holding_registers(0, 2)
if regs:
    print(regs)
else:
    print("read error")

# Write value 44 and 55 to registers at modbus address 10
list_of_values = [54,75] #decimal
is_write_ok = tcp_comm.write_multiple_registers(10, list_of_values)
if is_write_ok:
    print("write ok \n")
else:
    print("write error \n")

#Read coils
read_coils = tcp_comm.read_coils(0, 10)
fail = None
if read_coils != fail:
    print('coil ad #0 to 9: %s' % read_coils)
else:
    print('unable to read coils')

#Write coil
is_ok = tcp_comm.write_single_coil(0, 0)
if is_ok:
    print("write ok \n")
else:
    print("write error \n")

#*******************************************************************
#                    MODBUS TCP - CLIENT SERVICE
#*******************************************************************
'''
File name: modbusTCP_service.py
Description: This program implements a Modbus TCP client
    as service mode.
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
    * pyModbus Documentation:
        https://pypi.org/project/pyModbusTCP/
    * Systemd – Adicionando scripts na inicialização do Linux:
        https://embarcados.com.br/systemd-adicionando-scripts-na-inicializacao-do-linux/
    * Criando um serviço Linux
        https://blog.vepo.dev/posts/criando-um-servico-linux
    * Lista de comandos Linux
        https://github.com/LeandroTeodoroRJ/DicasLinux/blob/master/Comandos_Basicos.txt
Other Notes:
    * Run this as root to listen on TCP privileged ports (<= 1024).
    * To run
        sudo <full interpreter path> ./modbusTCP_service.py
        sudo /home/leandro/Dev/py3-10_modbusTCP/bin/python3 ./modbusTCP_service.py
    * To monitoring log file
        tail -f status.log
    * To create a systemd service
        Copy the service file to etc/systemd/system
        $systemctl enable modbusTCP_client.service
        $systemctl status modbusTCP_client.service
        $systemctl stop modbusTCP_client.service
        $systemctl start modbusTCP_client.service
        $systemctl restart modbusTCP_client.service
        $systemctl disable modbusTCP_client.service
'''

import time
import logging

from pyModbusTCP.client import ModbusClient

SERVER_HOST = "192.168.1.2"
SERVER_PORT = 502

# TCP auto connect on modbus request
tcp_comm = ModbusClient(host=SERVER_HOST, auto_open=True, unit_id=1, port=SERVER_PORT)

# init logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s, %(levelname)s, %(message)s",
    filename="status.log")

message = ""

#Start service
while True:
    #Read discrete inputs
    #Modbus funtion 0x02
    read_coils = tcp_comm.read_discrete_inputs(0, 10)
    fail = None
    if read_coils != fail:
        message = "input status ad 0 to 9:" + str(read_coils)
    else:
        message = "unable to read discrete inputs"
    logging.info(message)

    #Read input registers 2x 16 bits registers at modbus address 0
    #Modbus funtion 0x04
    regs = tcp_comm.read_input_registers(0, 2)
    fail = None
    if regs != fail:
        message = "input registers:" + str(regs)
    else:
        message = "read input registers error"
    logging.info(message)

    # 1s before to next loop
    time.sleep(1)

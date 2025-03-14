#*******************************************************************
#              MODBUS TCP - MYSQL DATABASE STORE
#*******************************************************************
'''
File name: modbusTCP_database.py
Description: This program implements a Modbus TCP to store Modbus
    TCP/IP PID control values in time series in MySQL.
URL to Download:
    https://github.com/LeandroTeodoroRJ/ModbusTCP-IP
Stable: Yes
Version: 1.0.0
Current: Yes
Maintainer: leandroteodoro.engenharia@hotmail.com
Depends:
    pyModbusTCP version: 0.3.0
	mysqlclient version: 2.2.7
	MySQL version: 8.0.41
Architecture: X86
Compile/Interpreter: python 3.10.12
Access: Public
Changelog: No changelog
Readme: No readme (inside this code)
Document Extra-Files:
    requirements.txt - Dependences Python VM
	schema.sql - Database PID schema to import
Links:
    pyModbus Documentation - https://pypi.org/project/pyModbusTCP/
    my2Collector - https://github.com/meob/my2Collector
Other Notes:
    * Run this as root to listen on TCP privileged ports (<= 1024).
    * To run
        sudo <full interpreter path>/bin/python3 ./modbusTCP_database.py
        sudo /home/ubuntu/Dev/modbus_tcp/bin/python3 ./modbusTCP_database.py

	*To create a Database in MySQL
		CREATE DATABASE PID;

	*To Create tables
CREATE TABLE IF NOT EXISTS status (
  VARIABLE_NAME varchar(64) CHARACTER SET utf8 NOT NULL DEFAULT '',
  VARIABLE_VALUE varchar(1024) CHARACTER SET utf8 DEFAULT NULL,
  HOST varchar(128) CHARACTER SET utf8 DEFAULT 'MyHost',   -- concat(@@hostname, ':', @@port),
  TIMEST timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS current (
  VARIABLE_NAME varchar(64) CHARACTER SET utf8 NOT NULL DEFAULT '',
  VARIABLE_VALUE varchar(1024) CHARACTER SET utf8 DEFAULT NULL
);

ALTER TABLE status ADD unique KEY idx01 (VARIABLE_NAME, timest);

ALTER TABLE current ADD unique KEY idx02 (VARIABLE_NAME);

mysql> describe status;
+----------------+---------------+------+-----+-------------------+-----------------------------------------------+
| Field          | Type          | Null | Key | Default           | Extra                                         |
+----------------+---------------+------+-----+-------------------+-----------------------------------------------+
| VARIABLE_NAME  | varchar(64)   | NO   | PRI |                   |                                               |
| VARIABLE_VALUE | varchar(1024) | YES  |     | NULL              |                                               |
| HOST           | varchar(128)  | YES  |     | MyHost            |                                               |
| TIMEST         | timestamp     | NO   | PRI | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
+----------------+---------------+------+-----+-------------------+-----------------------------------------------+

mysql> describe current;
+----------------+---------------+------+-----+---------+-------+
| Field          | Type          | Null | Key | Default | Extra |
+----------------+---------------+------+-----+---------+-------+
| VARIABLE_NAME  | varchar(64)   | NO   | PRI |         |       |
| VARIABLE_VALUE | varchar(1024) | YES  |     | NULL    |       |
+----------------+---------------+------+-----+---------+-------+

	*To export schema from database
		sudo mysqldump -u root -h localhost --no-data database_name > schema.sql
	*To import databse schema
		sudo mysql -u root -h localhost PID < schema.sql
	*Insert SQL values example
		INSERT INTO status VALUES('Set_Point', '123', DEFAULT, DEFAULT);
	*Create a database user
		CREATE USER 'store_client'@'localhost' IDENTIFIED BY 'fx3u';
		GRANT SELECT, INSERT, UPDATE, DELETE ON PID.* to 'store_client'@'localhost';
		FLUSH PRIVILEGES;
	*To see users
		USE mysql;
		SELECT user FROM user;
	*To see user privileges
		SHOW GRANTS FOR 'store_client'@'localhost';
'''

import time

from pyModbusTCP.client import ModbusClient
import MySQLdb

SERVER_HOST = "192.168.1.2"
SERVER_PORT = 502
TIME_TO_REQUEST = 1
START_HOLDING_ADDRESS = 0
NUMBER_HOLDING_REGISTERS = 5

holding_modbus_names = ["LEVEL METER", "FLOW METER", "SET POINT", "PID OUTPUT CONTROL", "ACTUATOR VALUE"]

# TCP auto connect on modbus request
tcp_comm = ModbusClient(host=SERVER_HOST, auto_open=True, unit_id=1, port=SERVER_PORT)

#MySQL Connect
db = MySQLdb.connect(host="localhost",    		 # your host, usually localhost
                     user="store_client",        # your username
                     password="fx3u",  			 # your password
                     db="PID")        			 # name of the data base

# you must create a Cursor object. It will let
# you execute all the queries you need
cursor = db.cursor()

#Start service
while True:
	#Read holding registers
	regs = tcp_comm.read_holding_registers(START_HOLDING_ADDRESS, NUMBER_HOLDING_REGISTERS)
	if regs:
		print(regs)

		for i in range(len(regs)):
			# SQL request
			sql = "INSERT INTO status VALUES(\"" + holding_modbus_names[i] + "\",\"" +  str(regs[i]) + "\"," + "DEFAULT, DEFAULT);"
			cursor.execute(sql)
			db.commit()

	else:
		print("read error")

	print("")
	# Time to next loop
	time.sleep(TIME_TO_REQUEST)

db.close()



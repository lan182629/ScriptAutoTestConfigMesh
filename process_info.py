import subprocess
import os
import datetime
import time
import csv
import telnetlib
import random
import threading
import winsound
from const import *

###
def check_ratio_loss_ping(ip_ping = 'none', count_request = 'none'):
    print("================================>Check Ping IP ",ip_ping)
    log_txt = subprocess.getoutput("ping " + ip_ping + " -n " + str(count_request) + " | findstr loss")
    print (log_txt)
    get_line = log_txt.split('\n')
    index_return = []
    try:
        for i in range(len(get_line[0])):
            if get_line[0][i] == '(':
                index_return.append(i)
                break
        for i in range(len(get_line[0])):
            if get_line[0][i] == '%':
                index_return.append(i)
                break
        return int(get_line[0][(index_return[0] + 1):index_return[1]])
    except:
        return 1000
###
def telnet_ont_ecnt_run_command(dir = '' , ip = '192.168.1.1', list_command = ['']):
    user_ont = 'admin'
    pass_ont = 'gpon@Mbf090'
    try:
        tn = telnetlib.Telnet(ip)
        tn.read_until(b"tc login: ")
        tn.write(user_ont.encode('ascii') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(pass_ont.encode('ascii') + b"\n")
        for command in list_command:
            tn.write(command.encode('ascii'))
            time.sleep(1)
        tn.write(b'exit\n')
        out_put = tn.read_all().decode('ascii')
        write_log_to_txt(dir, data_log =  out_put.replace("\n", ""))
        print("....................................DONE TELNET")
        return out_put
    except:
        out_put = "no info in except, KHONG TELNET DUOC ONT"
        print("Khong telnet duoc")
        write_log_to_txt(dir, data_log =  out_put)
        return out_put
###
def write_list_to_row_csv(dir = '', list_data = ['']):
    'WRITE LIST TO CSV WINDOWS'
    with open(dir, mode='a+',newline='') as file:
        csv_file = csv.writer(file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_file.writerow(list_data)
###
def write_log_to_txt(dir = '', data_log = ''):
    file = open(dir, "a+")
    file.write(data_log + '\n')
    file.close()
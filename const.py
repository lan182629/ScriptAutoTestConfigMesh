import subprocess
import os
import datetime
import time
import sys
import re
from process_info import *
USER = 'admin'
PASS_LOGIN = 'ttcn@99CN'
IP_ONT = '192.168.1.1'
URL_CONFIG_WIFI_2G = 'https://' + IP_ONT + '/cgi-bin/net-wlan.asp'
URL_CONFIG_WIFI_5G = 'https://' + IP_ONT + '/cgi-bin/net-wlan11ac.asp'
URL_REBOOT_ONT =  'https://' + IP_ONT + '/cgi-bin/tools_system.asp'
URL_DHCP_CLIENT = 'https://' + IP_ONT + '/cgi-bin/status_DHCP_Clients.asp'
URL_LOGOUT_DRAFT = 'https://' + IP_ONT + '/cgi-bin/logout.cgi'
VALUE_MODE_2G = ['b,g,n', 'b,g', 'n', 'g', 'b', 'g,n,ax']
VALUE_MODE_5G = [14,15,17]
VALUE_BAND_2G = [0,1,2]
VALUE_BAND_5G = [0,1]
VALUE_MODE_AUTHEN_2G = ['None', 'WPA', '11i', 'WPAand11i', 'WPA3-PSK', 'WPA2-PSK/WPA3-PSK']
VALUE_MODE_AUTHEN_5G = ['OPEN', 'WPAPSK', 'WPA2PSK', 'WPAPSKWPA2PSK', 'WPA3PSK', 'WPA2PSKWPA3PSK']
VALUE_MODE_AUTHEN_MESH_5G = ['WPAPSK', 'WPA2PSK', 'WPAPSKWPA2PSK', 'WPA3PSK', 'WPA2PSKWPA3PSK']
VALUE_CHANNEL_2G = [0,1,2,3,4,5,6,7,8,9,10,11]
VALUE_CHANNEL_5G = [0,36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165]
EVENT = ['OK', 'WARNING', 'CRITICAL', 'UNKNOW']
MAC_BACKHAUL = 'CC:71:90:4A:25:08'
PTIME_STAND = datetime.datetime.now().strftime("%H%M%S_%d%m%Y")
USER_SYS = subprocess.getoutput("echo %USERNAME%")
DIR_STAND = "C:\\Users\\" + USER_SYS +"\\Documents\\Wifi_check_ssid\\" 
DIR_FOLDER_STAND = DIR_STAND + "check_connect_mesh_" +PTIME_STAND + "\\"
DIR_FOLDER_TXT = DIR_FOLDER_STAND + PTIME_STAND + "_text_problem" + "\\"
DIR_FOLDER_JPG = DIR_FOLDER_STAND + PTIME_STAND + "_jpg_problem" + "\\"
DIR_FILE_LOG_SUMMARY = DIR_FOLDER_STAND + "check_connect_mesh_sum_" + PTIME_STAND + ".csv"
if ' ' in USER_SYS:
    print(" - --  ---   -----    ------")
    DIR_STAND_CREATE = "C:\\Users\\\"" + USER_SYS +"\"\\Documents\\Wifi_check_ssid\\" 
    os.system("md C:\\Users\\\"" + USER_SYS +"\"\\Documents\\Wifi_check_ssid\\")
    os.system("md C:\\Users\\\"" + USER_SYS +"\"\\Documents\\Wifi_check_ssid\\" + PTIME_STAND + "\\")
    os.system("md C:\\Users\\\"" + USER_SYS +"\"\\Documents\\Wifi_check_ssid\\" + PTIME_STAND + "\\text_problem\\")
    os.system("md C:\\Users\\\"" + USER_SYS +"\"\\Documents\\Wifi_check_ssid\\" + PTIME_STAND + "\\_jpg_problem\\")
else:
    print("-------")
    os.system("md " + DIR_STAND)
    os.system("md " + DIR_FOLDER_TXT)
    os.system("md " + DIR_FOLDER_JPG)
print("KHOI TAO FOLDER RESULT...")
LIST_RANDOM = [0,1,1,2,2,4,4,5,5,6,6,6,6]
time.sleep(2)
write_log_to_txt(dir = DIR_FOLDER_STAND + PTIME_STAND + "_info_mac.txt", data_log = MAC_BACKHAUL + '\n')
write_list_to_row_csv(dir = DIR_FILE_LOG_SUMMARY, list_data = ['[040M_mesh_v11072022]', 'ACTION', 'band', 'loss_ratio_ping', 'Delta Time', 'Result', '%lost Retest'])


from selenium import webdriver
from const import *
from webgui_ont import *
from process_info import *
import subprocess
import os
import ctypes
import datetime
import time
import sys
import random
import threading
###
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
###get_ip_mesh
web = webdriver.Chrome('C:\\chromedriver.exe', options = options)
wg_login(driver =  web, ip = IP_ONT)
IP_MESH = wg_get_ip_client_by_mac(web, URL_DHCP_CLIENT, MAC_BACKHAUL)
wg_logout(web, IP_ONT)
web.quit()
print("\n\n\n\nTien hanh check ket noi mesh, IP BACKHAUL: ", IP_MESH)
time.sleep(5)
###
count = 0
time_error = 0
check_stop = 0
while 1:
    count = count +1
    check = 0
#     random_int = random.randint(1,7)
    random_int = random.choice(LIST_RANDOM)
    print("\n\n===================\ncount:",count,"random = ",random_int)
    print("===================\n")
    time_current =  datetime.datetime.now().strftime("%H%M%S_%d%m%Y")
    print("Times error: ",time_error)
    print("dir_log: ",DIR_FILE_LOG_SUMMARY)
    print("\n[XXX]================",time_current,"================[XXX]")
    list_data = [time_current]
    web = webdriver.Chrome('C:\\chromedriver.exe', options = options)
    wg_login(driver =  web, ip = IP_ONT)
    web.get(URL_CONFIG_WIFI_5G)
    print("\n\n\n......................")
    if random_int %8 == 0:
        print("not_change_and_save_config_wifi_5Ghz")
        list_data.append('not_change_and_save_config_wifi_5Ghz')
        wg_save_config_wifi(driver = web, url_link = URL_CONFIG_WIFI_5G)
        list_data.append('5ghz')
        print(list_data)
    elif random_int %8 == 1:
        print("edit name wifi 5G")
        data_log = wg_edit_name_ssid_wifi(driver = web, name_wifi= time_current, flag_save_config = 1)
        list_data.append("edit name SSID wifi 5G_" + data_log)
        list_data.append('5ghz')
        print(list_data)
    elif random_int %8 == 2:
        print("edit channel wifi 5G")
        data_log = wg_wf_config_channel(web, VALUE_CHANNEL_5G, flag_save_config = 1)
        list_data.append("edit channel SSID 5G_" + data_log)
        list_data.append('5ghz')
        print(list_data)
    elif random_int %8 == 3:
        print("edit mode wifi 5G")
        data_log = wg_wf_config_mode(web, VALUE_MODE_5G, flag_save_config = 1)
        list_data.append("edit mode SSID 5G_" + data_log)
        list_data.append('5ghz') 
        print(list_data)
    elif random_int %8 == 4:
        print("edit bandwidth wifi 5G")
        data_log = wg_wf_config_bw_5g(web, VALUE_BAND_5G, flag_save_config = 1)
        list_data.append("edit bandwidth SSID 5G_" + data_log)
        list_data.append('5ghz') 
        print(list_data)
    elif random_int %8 == 5:
        print("edit authen wifi 5G")
        data_log = wg_wf_config_authen_5g(web, VALUE_MODE_AUTHEN_MESH_5G, time_current, flag_save_config = 1)
        list_data.append("edit authen SSID 5G_" + data_log)
        list_data.append('5ghz') 
        print(list_data)
    elif random_int %8 == 6:
        print("edit 4 agr wifi 5G")
        data_log = wg_config_all_wireless_5ghz(web, enable_config_name =1 , value_name_ssid = time_current, value_flag_band = 5,\
                                                enable_config_authen_ssid = 1, value_mode_authen_ssid = VALUE_MODE_AUTHEN_MESH_5G, value_pw= time_current,\
                                                enable_config_channel_ssid = 1, value_channel_ssid = VALUE_CHANNEL_5G, \
                                                enable_config_mode_ssid = 0, value_mode_ssid = VALUE_MODE_5G, \
                                                enable_bw_ssid = 1, value_bw_channel = VALUE_BAND_5G)
        list_data.append("edit_4_args:" + data_log)
        list_data.append('5ghz')
        print(list_data)
    else:
        print("edit all agr wifi 5G")
        data_log = wg_config_all_wireless_5ghz(web, enable_config_name =1 , value_name_ssid = time_current, value_flag_band = 5,\
                                                enable_config_authen_ssid = 1, value_mode_authen_ssid = VALUE_MODE_AUTHEN_MESH_5G, value_pw= time_current,\
                                                enable_config_channel_ssid = 1, value_channel_ssid = VALUE_CHANNEL_5G, \
                                                enable_config_mode_ssid = 1, value_mode_ssid = VALUE_MODE_5G, \
                                                enable_bw_ssid = 1, value_bw_channel = VALUE_BAND_5G)
        list_data.append("edit_5_args:" + data_log)
        list_data.append('5ghz')
        print(list_data)
    time.sleep(2)
    wg_logout(web, IP_ONT)  
    web.quit()
    time_start = time.time()
    print("\n[***]sleep 35s")
    time.sleep(25)
    dir_log_telnet = DIR_FOLDER_TXT + '{' + str(count) + "}_" + time_current + "_telnet.txt"
    command_telnet = ['tcapi show wlan\n',  'tcapi show wlan11ac\n', 'uptime\n']
    thread_tn = threading.Thread(target=telnet_ont_ecnt_run_command, \
                                args=(dir_log_telnet, IP_ONT, command_telnet,))   
    thread_tn.start()
    thread_tn.join(0)
    time.sleep(10)
    print("\n\n\n\nTien hanh check ket noi mesh, IP BACKHAUL: ", IP_MESH)
    while(1):
        delta_time = int(time.time() - time_start)
        check = check + 1
        loss_ratio = check_ratio_loss_ping(ip_ping = IP_MESH, count_request = 3)
        if delta_time <= 1200:
            if loss_ratio == 0:
                print("\n@@@@@@@@@\nPING OK INTERFACE MESH\n@@@@@@@@@")
                list_data = list_data + [loss_ratio] + [delta_time] + [EVENT[0]]
                print("Wait 25s cho lan tiep theo, lost ratio = ", loss_ratio, ('%'))
                time.sleep(25)
                loss_ratio_retest = check_ratio_loss_ping(ip_ping = IP_MESH, count_request = 10)
                if 0 <= loss_ratio_retest <= 20:
                    print("................retest OK")
                else:
                    check_stop = check_stop + 1    
                    print("\n\n\n\n----------------------------------> RETEST THAT BAI")
                list_data = list_data + [str(loss_ratio_retest)] 
                write_list_to_row_csv(dir = DIR_FILE_LOG_SUMMARY, list_data = list_data)
                break
            else:
                continue
        else:
            if 0 < loss_ratio < 60:
                print("\n@@@@@@@@@\nPING DUOC INTERFACE MESH, co LOSS\n@@@@@@@@@")
                list_data = list_data + [loss_ratio] + [delta_time] + [EVENT[1]]
                print("Wait 25s cho lan tiep theo, lost ratio = ", loss_ratio, ('%'))
                time.sleep(25)
                loss_ratio_retest = check_ratio_loss_ping(ip_ping = IP_MESH, count_request = 10)
                if 0 <= loss_ratio_retest <= 20:
                    print("................retest OK")
                else:
                    check_stop = check_stop + 1    
                    print("\n\n\n\n----------------------------------> RETEST THAT BAI")
                list_data = list_data + [str(loss_ratio_retest)]
                write_list_to_row_csv(dir = DIR_FILE_LOG_SUMMARY, list_data = list_data)
                break
            else:
                print("\n@@@@@@@@@\nKHONG PING DUOC INTERFACE MESH\n@@@@@@@@@")
                list_data = list_data + [loss_ratio] + [delta_time] + [EVENT[2]]
                write_list_to_row_csv(dir = DIR_FILE_LOG_SUMMARY, list_data = list_data)
                check_stop = check_stop + 1
                break
    if check_stop == 1:
        print("MAT KET NOI MESH")
        break
    os.system("cls")
print("DONE DONE")
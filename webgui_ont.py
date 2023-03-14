from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium
import time
import random
import re
###
EVENT = ['OK', 'WARNING', 'CRITICAL', 'UNKNOW']
###
def wg_login(driver , ip , user ='admin', passwd = 'ttcn@99CN'):
    driver.set_page_load_timeout(45)
    try:
        driver.implicitly_wait(45)
        driver.get("https://"+ip+"/cgi-bin/login.asp")
        time.sleep(2)
        elem = driver.find_element_by_id('username')
        elem.clear()
        elem.send_keys(user)
        time.sleep(1)
        elem = driver.find_element_by_id('password')
        elem.clear()
        elem.send_keys(passwd)
        time.sleep(1)
        elem.send_keys(Keys.RETURN)
        time.sleep(1)    
        print("Login OK")
        return EVENT[0]
    except:
        print("Khong login duoc")
        return EVENT[1]
###
def wg_config_all_wireless_5ghz(driver, \
#                           enable_config_index = 0, value_index = 'none', \
                          enable_config_name = 1, value_name_ssid = 'none', value_flag_band = 5, \
                          enable_config_authen_ssid = 1, value_mode_authen_ssid = 'none', value_pw = 'none_none', \
                          enable_config_channel_ssid = 1, value_channel_ssid = 'none', \
                          enable_config_mode_ssid = 1, value_mode_ssid = 'none', \
                          enable_bw_ssid = 1, value_bw_channel = 'none'):
    driver.implicitly_wait(45)
    result_actions = ''
    if enable_config_name == 1:
        data_return = wg_edit_name_ssid_wifi(driver, name_wifi = value_name_ssid, flag_band= value_flag_band, flag_save_config = 0)
        result_actions = result_actions + '_' + data_return
    if enable_config_authen_ssid == 1:
        data_return = wg_wf_config_authen_5g(driver, value_list_mode_authen = value_mode_authen_ssid,  value_password = value_pw, flag_save_config = 0)
        result_actions = result_actions + '_' + data_return
    if enable_config_channel_ssid ==  1:
        data_return = wg_wf_config_channel(driver, value_list_channel = value_channel_ssid, flag_save_config = 0)
        result_actions = result_actions + '_' + data_return
    if enable_config_mode_ssid == 1:
        data_return = wg_wf_config_mode(driver, value_list_mode = value_mode_ssid, flag_save_config = 0)
        result_actions = result_actions + '_' + data_return
    if enable_bw_ssid == 1:
        data_return = wg_wf_config_bw_5g(driver, value_list_bw = value_bw_channel, flag_save_config = 0)
        result_actions = result_actions + '_' + data_return
    time.sleep(1)
    driver.find_element_by_id('btnOK').click()
    return result_actions
###
def wg_wf_config_bw_5g(driver, value_list_bw = 'none', flag_save_config = 1):
    # cur_value_mode_wifi = driver.find_element_by_xpath("//select[@name='WirelessMode']/option[@selected]").get_attribute("value")
    try:
        cur_value_bw_wifi = driver.find_element_by_xpath("//select[@name='WLan11acVHTChannelBandwidth']/option[@selected]").text
        try:
            print("Bandwidth wifi hien tai: ", cur_value_bw_wifi)
            while(1):
                find_text_mode = ''
                bandwidth = random.choice(value_list_bw)
                find_text_mode = driver.find_element_by_xpath("//select[@name='WLan11acVHTChannelBandwidth']/option[@value='"+str(bandwidth)+"']").text
                time.sleep(1)
                if find_text_mode != cur_value_bw_wifi:
                    print("----------------------------> edit bandwidth wireless sang: ", find_text_mode)
                    break
        except:
            print("khong get duoc bandwidth wifi")
        print("..................Modify bandwidth wifi")
        driver.find_element_by_xpath("//select[@name='WLan11acVHTChannelBandwidth']/option[@value='"+str(bandwidth)+"']").click()
        time.sleep(1)
        try:
            time.sleep(1)
            alert = driver.switch_to_alert()
            alert.accept()
            print("alert accepted")
        except:
            print("no alert")
        if flag_save_config == 1:
            driver.find_element_by_id('btnOK').click()
        return re.sub('[^A-Za-z0-9]+', '', cur_value_bw_wifi) + "_to_" + re.sub('[^A-Za-z0-9]+', '', find_text_mode) + '_OK'
    except:
        print("Edit mode wl failed")
        return "Edit mode wl failed"
###
def wg_wf_config_mode(driver, value_list_mode = 'none', flag_save_config = 1):
    try:
        cur_text_mode = driver.find_element_by_xpath("//select[@name='WirelessMode']/option[@selected]").text
        try:
            print("Mode wifi hien tai: ", cur_text_mode)
            while(1):
                find_text_mode = ''
                mode = random.choice(value_list_mode)
                find_text_mode = driver.find_element_by_xpath("//select[@name='WirelessMode']/option[@value='"+str(mode)+"']").text
                time.sleep(1)
                if find_text_mode != cur_text_mode:
                    print("----------------------------> edit mode wireless sang: ", find_text_mode)
                    break
        except:
            print("khong get duoc mode")
        print("..................Modify mode wifi")
        driver.find_element_by_xpath("//select[@name='WirelessMode']/option[@value='"+str(mode)+"']").click()
        time.sleep(1)
        try:
            time.sleep(1)
            alert = driver.switch_to_alert()
            alert.accept()
            print("alert accepted")
        except:
            print("no alert")
        if flag_save_config == 1:
            driver.find_element_by_id('btnOK').click()
        return re.sub('[^A-Za-z0-9]+', '', cur_text_mode) + "_to_" + re.sub('[^A-Za-z0-9]+', '', find_text_mode) + '_OK'
    except:
        print("Edit mode wl failed")
        return "Edit mode wl failed"
###
def wg_wf_config_channel(driver, value_list_channel = 'none', flag_save_config = 1):
    try:
        cur_text_channel = driver.find_element_by_name('CurrentChannel').get_attribute("value")
        try:
            print("Channel hien tai: ", cur_text_channel)
            while(1):
                text_channel_result = ''
                channel_wf = random.choice(value_list_channel)
                text_channel_result = driver.find_element_by_xpath("//select[@name='Channel_ID']/option[@value='"+str(channel_wf)+"']").text
                time.sleep(1)
                if text_channel_result != cur_text_channel:
                    print("----------------------------> edit channel sang: ", text_channel_result)
                    break
        except:
            print("khong get duoc mode")
        driver.find_element_by_xpath("//select[@name='Channel_ID']/option[@value='"+str(channel_wf)+"']").click()
        try:
            time.sleep(1)
            alert = driver.switch_to_alert()
            alert.accept()
            print("alert accepted")
        except:
            print("no alert")
        if flag_save_config == 1:
            driver.find_element_by_id('btnOK').click()
        return 'channel:' + cur_text_channel + "_to_channel:" + text_channel_result + '_OK'
    except:
        print("Edit Channel wireless failed")
        return "Edit Channel wireless failed" 
##
def wg_wf_config_authen_5g(driver, value_list_mode_authen = 'none', value_password = 'none_none', flag_save_config = 1):
    try:
        cur_text_mode = driver.find_element_by_xpath("//select[@name='WEP_Selection']/option[@selected]").text
        try:
            print("Mode hien tai: ", cur_text_mode)
            while(1):
                find_text_mode = ''
                mode = random.choice(value_list_mode_authen)
                find_text_mode = driver.find_element_by_xpath("//select[@name='WEP_Selection']/option[@value='"+str(mode)+"']").text
                time.sleep(1)
                if find_text_mode != cur_text_mode:
                    print("----------------------------> edit mode wireless sang: ", find_text_mode)
                    break
        except:
            print("khong get duoc mode")
        print("..................Modify authen mode wifi")
        driver.find_element_by_xpath("//select[@name='WEP_Selection']/option[@value='"+str(mode)+"']").click()
        time.sleep(1)
        try:
            time.sleep(1)
            ale = driver.switch_to_alert()
            ale.accept()
            print("alert accepted")
        except:
            print("no alert")
        data_return = re.sub('[^A-Za-z0-9]+', '', cur_text_mode) + "_to_" + re.sub('[^A-Za-z0-9]+', '', find_text_mode) + '_OK'
        if value_password != 'none_none':
            wg_edit_password_authen(driver, mode, value_password)
            data_return = data_return + '_pw:' + value_password +':OK'
        if flag_save_config == 1:
            driver.find_element_by_id('btnOK').click()
        print('DATA:....................................', data_return)
        return data_return
    except:
        print("Edit authen mode wireless failed")
        return "Edit authen mode wireless failed"  
###
def wg_edit_password_authen(driver, mode_authen, value_password = 'none_none'):
    if mode_authen == 'WPAPSK':    
        elem = driver.find_element_by_name('PreSharedKey2')
        elem.clear()
        try:
            time.sleep(1)
            alert = driver.switch_to_alert()
            alert.accept()
            print("alert accepted")
        except:
            print("no alert")
        elem.send_keys(value_password)
        print("change password to: ", value_password)
    elif mode_authen == 'WPA2PSK': 
        elem = driver.find_element_by_name('PreSharedKey1')
        elem.clear()
        try:
            time.sleep(1)
            alert = driver.switch_to_alert()
            alert.accept()
            print("alert accepted")
        except:
            print("no alert")
        elem.send_keys(value_password)
        print("change password to: ", value_password)
    elif mode_authen == 'WPAPSKWPA2PSK': 
        elem = driver.find_element_by_name('PreSharedKey3')
        elem.clear()
        try:
            time.sleep(1)
            alert = driver.switch_to_alert()
            alert.accept()
            print("alert accepted")
        except:
            print("no alert")
        elem.send_keys(value_password)
        print("change password to: ", value_password)
    elif mode_authen == 'WPA3PSK': 
        elem = driver.find_element_by_name('PreSharedKey_WPA3')
        elem.clear()
        try:
            time.sleep(1)
            alert = driver.switch_to_alert()
            alert.accept()
            print("alert accepted")
        except:
            print("no alert")
        elem.send_keys(value_password)
        print("change password to: ", value_password)
    else:
        'WPA2PSKWPA3PSK'
        elem = driver.find_element_by_name('PreSharedKey_WPA2WPA3')
        elem.clear()
        try:
            time.sleep(1)
            alert = driver.switch_to_alert()
            alert.accept()
            print("alert accepted")
        except:
            print("no alert")
        elem.send_keys(value_password)
        print("change password to: ", value_password)
###    
def wg_edit_name_ssid_wifi(driver, name_wifi, flag_band = 5, flag_save_config = 1):
    driver.set_page_load_timeout(45)
    try:
        driver.implicitly_wait(45)
        if flag_band == 2:
            elem = driver.find_element_by_name('wlSsid')
            elem.clear()
            time.sleep(1)
            elem.send_keys(name_wifi)
            time.sleep(1)
        elif flag_band == 5:
            elem = driver.find_element_by_name('ESSID')
            elem.clear()
            time.sleep(1)
            elem.send_keys(name_wifi)
            time.sleep(1)
        print("..................Modify name ssid wifi")
        time.sleep(1)
        if flag_save_config == 1:
            driver.find_element_by_id('btnOK').click()
        print("Edit name Wifi Wifi OK")
        return EVENT[0]
    except:
        print("Edit name SSID Failed")
        return "Edit name SSID Failed"
    
###
def wg_save_config_wifi(driver, url_link):
    driver.set_page_load_timeout(45)
    try:
        driver.implicitly_wait(45)
        driver.get(url_link)
        time.sleep(2)
        # driver.find_element_by_id('btnOK').click()
        # elem = driver.find_element_by_xpath("//select[@id='btnOK']/option[@value='SAVE']").click()
        print("SAVE Config Wifi OK")
        return EVENT[0]
    except:
        print("Save config Failed")
        return EVENT[1]    
###
def wg_logout(driver, ip_ont):
    url_link = 'https://' + ip_ont + '/cgi-bin/logout.cgi'
    driver.get(url_link)
    time.sleep(2)
###
def wg_get_ip_client_by_mac(driver, url_link, mac_address):
    driver.set_page_load_timeout(45)
    i = 1
    check_break = 0
    driver.get(url_link)
    while(1):
        try:
            j = 1
            while(j < 6):
                try:
                    value = driver.find_element_by_xpath("//*[@id='client_list']/tbody/tr[" + str(i) + "]/td[" + str(j) + "]").text
                    # print("Value = ", value)
                    if value == mac_address:
                        ip_client = driver.find_element_by_xpath("//*[@id='client_list']/tbody/tr[" + str(i) + "]/td[" + str(j+1) + "]").text
                        # print("IP_CLIEN: ", ip_client)
                        check_break = 1
                        break
                    j = j + 1
                except:
                    break
            i = i + 1
            if check_break == 1:
                print("IP client MAC ", mac_address, ":.........", ip_client)
                return ip_client
                time.sleep(2)
                break
        except:
            print("IP client MAC ", mac_address, ": NONE")
            return 'none'
            break
###    
    
    

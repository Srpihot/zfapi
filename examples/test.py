#coding=utf-8
import time
from zfapi import Login
from zfapi import GetInfo

base_url = 'http://112.5.137.43:9993/jwglxt/'
username = '1801130030'
password = 'sph2018dbtx'
count = 0
while count<=3:
    try:
        lgn = Login(base_url = base_url)
        lgn.login(username,password)
        cookies = lgn.cookies 
        srpihot = GetInfo(base_url=base_url, cookies=cookies)
        print("====个人信息====")
        print(srpihot.get_information_raw())
        break
    except Exception as e:
        print('[Error]',e)
        time.sleep(3)
        count += 1
#coding=utf-8
import time
from zfapi import Login
from zfapi import GetInfo

base_url = 'http://xxxxx/'
username = 'xxxx'
password = 'xxxx'
count = 0
while count<=3:
    try:
        lgn = Login(base_url = base_url)
        lgn.login(username,password)
        cookies = lgn.cookies 
        srpihot = GetInfo(base_url=base_url, cookies=cookies)
        print("====个人信息====")
        print(srpihot.get_information())
        print("====消息====")
        print(srpihot.get_message())
        print("====考试信息====")
        print(srpihot.get_exam('2020','1'))
        print("====课程表====")
        print(srpihot.get_schedule('2020','1'))
        print("====个人成绩====")
        print(srpihot.get_grade('2020','1'))
        print("====通知====")
        print(srpihot.get_notice())
        print("====正方原始个人信息json格式====")
        print(srpihot.get_information_raw())
        print("====正方原始消息json格式====")
        print(srpihot.get_message())
        print("====正方原始考试信息json格式====")
        print(srpihot.get_exam('2020','1'))
        print("====正方原始课程表json格式====")
        print(srpihot.get_schedule('2020','1'))
        print("====正方原始个人成绩json格式====")
        print(srpihot.get_grade('2020','1'))
        break
    except Exception as e:
        print('[Error]',e)
        time.sleep(3)
        count += 1
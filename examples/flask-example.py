# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
from flask import Flask, request, jsonify
from zfapi import Login
from zfapi import GetInfo

app = Flask(__name__)
SCHOOL_URL = 'http://120.35.34.241:8443/jwglxt/'


@app.route('/get_info')
def get_info():
    # 获取存用户信息
    # param:
    #   user : 学号
    #   passwd : 密码
    # http://127.0.0.1:5000/get_info?user=XXX&passwd=XXX
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    cookies = init(user,passwd)
    result = GetInfo(base_url=SCHOOL_URL, cookies=cookies).get_information()
    return jsonify(resul.get_information_raw())

@app.route('/get_info_raw')
def get_info_raw():
    # 获取存用户信息
    # param:
    #   user : 学号
    #   passwd : 密码
    # http://127.0.0.1:5000/get_info?user=XXX&passwd=XXX
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    cookies = init(user,passwd)
    result = GetInfo(base_url=SCHOOL_URL, cookies=cookies).get_information_raw()
    return jsonify(resul.get_information_raw())

@app.route('/get_score_avg')
def get_score_avg():
    # 获取一学年平均成绩
    # param:
    #   user : 学号
    #   passwd : 密码
    #   year : 学年（2019-2020 2020）
    #   term : 学期
    # http://127.0.0.1:5000/get_score?user=XXX&passwd=XXX&year=2020&term=2
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    year = request.args.get("year")
    # term = request.args.get("term")
    cookies = init(user,passwd)
    results = {}
    result = GetInfo(base_url=SCHOOL_URL, cookies=cookies)
    grade_up = result.get_grade(year,'1')
    grade_total_up = 0.0
    credit_total_up = 0.0
    for i in range (0,len(grade_up['course'])):
        courses = grade_up['course']
        credit= float(courses[i]['credit'])
        grade = float(courses[i]['gradePoint'])*10.0 + 50.0
        # print(courses[i]['className'],end=' ')
        # print(grade,credit)
        grade_total_up += grade * credit
        credit_total_up += credit
    grade_up = grade_total_up/credit_total_up

    results['first_score'] = str(grade_total_up/credit_total_up)
    results['first_GPA'] = str((grade_total_up * 4)/(credit_total_up * 100.0))
    
    grade_down = result.get_grade(year,'2')
    grade_total_down = 0.0
    credit_total_down = 0.0
    for i in range (0,len(grade_down['course'])):
        if '高级数据库' in courses[i]['className']:
            continue
        courses = grade_down['course']
        credit= float(courses[i]['credit'])
        grade = float(courses[i]['gradePoint'])*10.0 + 50.0
        # print(courses[i]['className'],end=' ')
        # print(grade,credit)
        grade_total_down += grade * credit
        credit_total_down += credit
    grade_down = grade_total_down/credit_total_down

    # print('the second term exam grade:'+str(grade_total_down/credit_total_down))
    # print('the first term GPA:'+ str((grade_total_down * 4)/(credit_total_down * 100.0)))
    # print('the total term avg exam grade:'+str((grade_total_up+grade_total_down)/(credit_total_up+credit_total_down)))
    # print('the total term GPA:'+ str(((grade_total_up+grade_total_down)*4.0)/((credit_total_up+credit_total_down) *100.0 ) ))
    results['second_score'] = str(grade_total_down/credit_total_down)
    results['second_GPA'] = str((grade_total_down * 4)/(credit_total_down * 100.0))
    results['total_score'] = str((grade_total_up+grade_total_down)/(credit_total_up+credit_total_down))
    results['total_GPA'] = str(((grade_total_up+grade_total_down)*4.0)/((credit_total_up+credit_total_down) *100.0 ) )
    
    return jsonify(results)

@app.route('/get_score')
def get_score():
    # 获取成绩
    # param:
    #   user : 学号
    #   passwd : 密码
    #   year : 学年
    #   term : 学期
    # http://127.0.0.1:5000/get_score?user=XXX&passwd=XXX&year=2020&term=2
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    year = request.args.get("year")
    term = request.args.get("term")
    cookies = init(user,passwd)
    result = GetInfo(base_url=SCHOOL_URL, cookies=cookies).get_grade(year,term)
    return jsonify(result)

@app.route('/get_score_raw')
def get_score_raw():
    # 获取成绩
    # param:
    #   user : 学号
    #   passwd : 密码
    #   year : 学年
    #   term : 学期
    # http://127.0.0.1:5000/get_score?user=XXX&passwd=XXX&year=2020&term=2
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    year = request.args.get("year")
    term = request.args.get("term")
    cookies = init(user,passwd)
    result = GetInfo(base_url=SCHOOL_URL, cookies=cookies).get_grade_raw(year,term)
    return jsonify(result)


@app.route('/get_schedule')
def get_schedule():
    # 获取课程表
    # param:
    #   user : 学号
    #   passwd : 密码
    #   year : 学年
    #   term : 学期
    # http://127.0.0.1:5000/get_schedule?user=XXX&passwd=XXX&year=2020&term=2
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    year = request.args.get("year")
    term = request.args.get("term")
    cookies = init(user,passwd)
    result = GetInfo(base_url=SCHOOL_URL, cookies=cookies).get_schedule(year,term)
    return jsonify(result)

@app.route('/get_schedule_raw')
def get_schedule_raw():
    # 获取课程表
    # param:
    #   user : 学号
    #   passwd : 密码
    #   year : 学年
    #   term : 学期
    # http://127.0.0.1:5000/get_schedule?user=XXX&passwd=XXX&year=2020&term=2
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    year = request.args.get("year")
    term = request.args.get("term")
    cookies = init(user,passwd)
    result = GetInfo(base_url=SCHOOL_URL, cookies=cookies).get_schedule_raw(year,term)
    return jsonify(result)

@app.route('/get_notice')
def get_notice():
    # 获取正方系统通知
    # param:
    #   user : 学号
    #   passwd : 密码
    # http://127.0.0.1:5000/get_notice?user=XXX&passwd=XXX
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    cookies = init(user,passwd)
    result = GetInfo(base_url=SCHOOL_URL, cookies=cookies).get_notice()
    return jsonify(result)


@app.route('/get_message')
def get_message():
    # 获取信息（调课）
    # param:
    #   user : 学号
    #   passwd : 密码
    #   year : 学年
    #   term : 学期
    # http://127.0.0.1:5000/get_notice?user=XXX&passwd=XXX
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    cookies = init(user,passwd)
    result = GetInfo(base_url=SCHOOL_URL, cookies=cookies).get_message()
    return jsonify(result)

@app.route('/get_message_raw')
def get_message_raw():
    # 获取信息（调课）
    # param:
    #   user : 学号
    #   passwd : 密码
    #   year : 学年
    #   term : 学期
    # http://127.0.0.1:5000/get_notice?user=XXX&passwd=XXX
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    cookies = init(user,passwd)
    result = GetInfo(base_url=SCHOOL_URL, cookies=cookies).get_message_raw()
    return jsonify(result)

def init(username,password):
    lgn = Login(base_url = SCHOOL_URL)
    lgn.login(username,password)
    cookies = lgn.cookies 
    return cookies



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

#coding=utf-8
from bs4 import BeautifulSoup
import re
import time
import requests
from urllib import parse


class GetInfo(object):
    def __init__(self, base_url, cookies):
        self.base_url = base_url
        self.headers = {
            'Referer': base_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
        self.cookies = cookies

    def get_information(self):
        """获取个人信息"""
        url = parse.urljoin(self.base_url, 'xsxxxggl/xsxxwh_cxCkDgxsxx.html?gnmkdm=N100801')
        # print(url)
        res = requests.get(url, headers=self.headers, cookies=self.cookies)
        jres = res.json()
        # print(jres)
        res_dict = {
            'name': jres['xm'],
            'studentId': jres['xh'],
            'sex':jres['xbm'],
            'birthplace':jres['jg'],
            'email':jres['dzyx'],
            'telphone':jres['gddh'],
            'brithday': jres['csrq'],
            'idNumber': jres['zjhm'],
            'candidateNumber': jres['ksh'],
            'bankcard' : jres['yhkh'],
            'status': jres['xjztdm'],
            'collegeName': jres['zsjg_id'],
            'majorName': jres['zszyh_id'],
            'className': jres['bh_id'],
            'entryDate': jres['rxrq'],
            'graduationSchool': jres['byzx'],
            'domicile': jres['jtdz'],
            'politicalStatus': jres['zzmmm'],
            'national': jres['mzm'],
            'education': jres['pyccdm'],
            'postalCode': jres['yzbm']
        }
        return res_dict
    
    def get_information_raw(self):
        """获取原始正方数据个人信息"""
        url = parse.urljoin(self.base_url, 'xsxxxggl/xsxxwh_cxCkDgxsxx.html?gnmkdm=N100801')
        # print(url)
        res = requests.get(url, headers=self.headers, cookies=self.cookies)
        jres = res.json()
        return jres

    def get_notice(self):
        """获取通知"""
        url_0 = parse.urljoin(self.base_url, 'xtgl/index_cxNews.html?localeKey=zh_CN&gnmkdm=index')
        url_1 = parse.urljoin(self.base_url, 'xtgl/index_cxAreaTwo.html?localeKey=zh_CN&gnmkdm=index')
        res_list = []
        url_list = []

        res_0 = requests.get(url_0, headers=self.headers, cookies=self.cookies)
        res_1 = requests.get(url_1, headers=self.headers, cookies=self.cookies)
        soup_0 = BeautifulSoup(res_0.text, 'lxml')
        soup_1 = BeautifulSoup(res_1.text, 'lxml')
        url_list += [i['href'] for i in soup_0.select('a[href*="/xtgl/"]')]
        url_list += [i['href'] for i in soup_1.select('a[href*="/xtgl/"]')]

        for u in url_list:
            # print(parse.urljoin(self.base_url,u))
            _res = requests.get(parse.urljoin(self.base_url,u), headers=self.headers, cookies=self.cookies)
            _soup = BeautifulSoup(_res.text, 'lxml')
            title = _soup.find(attrs={'class': 'text-center'}).string
            info = [i.string for i in _soup.select_one('[class="text-center news_title1"]').find_all('span')]
            publisher = re.search(r'：(.*)', info[0]).group(1)
            ctime = re.search(r'：(.*)', info[1]).group(1)
            vnum = re.search(r'：(.*)', info[2]).group(1)
            detailed = _soup.find(attrs={'class': 'news_con'})
            content = ''.join(list(detailed.strings))
            doc_urls = [self.base_url + i['href'][2:] for i in detailed.select('a[href^=".."]')]
            res_list.append({
                'title': title,
                'publisher': publisher,
                'ctime': ctime,
                'vnum': vnum,
                'content': content,
                'doc_urls': doc_urls
            })
        return res_list

    def get_message(self):
        """获取消息"""
        url = parse.urljoin(self.base_url, 'xtgl/index_cxDbsy.html?doType=query')
        data = {
            'sfyy': '0',  # 是否已阅，未阅为1，已阅为2
            'flag': '1',
            '_search': 'false',
            'nd': int(time.time()*1000),
            'queryModel.showCount': '1000',  # 最多条数
            'queryModel.currentPage': '1',  # 当前页数
            'queryModel.sortName': 'cjsj',
            'queryModel.sortOrder': 'desc',  # 时间倒序, asc正序
            'time': '0'
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
        jres = res.json()
        res_list = [{'message': i['xxnr'], 'ctime': i['cjsj']} for i in jres['items']]
        return res_list

    def get_message_raw(self):
        """获取原始正方系统消息json信息"""
        url = parse.urljoin(self.base_url, 'xtgl/index_cxDbsy.html?doType=query')
        data = {
            'sfyy': '0',  # 是否已阅，未阅为1，已阅为2
            'flag': '1',
            '_search': 'false',
            'nd': int(time.time()*1000),
            'queryModel.showCount': '1000',  # 最多条数
            'queryModel.currentPage': '1',  # 当前页数
            'queryModel.sortName': 'cjsj',
            'queryModel.sortOrder': 'desc',  # 时间倒序, asc正序
            'time': '0'
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
        jres = res.json()
        return jres

    def get_grade(self, year, term):
        """获取成绩"""
        url = parse.urljoin(self.base_url, 'cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005')
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        elif term == '0':
            term = ''
        else:
            print('Please enter the correct term value！！！ ("0" or "1" or "2")')
            return {}
        data = {
            'xnm': year,  # 学年数
            'xqm': term,  # 学期数，第一学期为3，第二学期为12, 整个学年为空''
            '_search': 'false',
            'nd': int(time.time()*1000),
            'queryModel.showCount': '100',  # 每页最多条数
            'queryModel.currentPage': '1',
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
            'time': '0'  # 查询次数
        }
        res = requests.post(url = url, headers=self.headers, data=data, cookies=self.cookies)
        jres = res.json()
        if jres.get('items'):  # 防止数据出错items为空
            res_dict = {
                'name': jres['items'][0]['xm'],
                'studentId': jres['items'][0]['xh'],
                'schoolYear': jres['items'][0]['xnm'],
                'schoolTerm': jres['items'][0]['xqmmc'],
                'course': [{
                    'courseTitle': i['kcmc'],
                    'teacher': i['jsxm'],
                    'courseId': i['kch_id'],
                    'className': i['jxbmc'],
                    'courseNature': ''if i.get('kcxzmc')== None else i.get('kcxzmc'),
                    'credit': i['xf'],
                    'grade': i['cj'],
                    'gradePoint': '' if i.get('jd') == None else i.get('jd'),
                    'gradeNature': i['ksxz'],
                    'startCollege': i['kkbmmc'],
                    'courseMark': i['kcbj'],
                    'courseCategory': i['kclbmc'],
                    'courseAttribution': '' if i.get('kcgsmc') == None else i.get('kcgsmc')
                } for i in jres['items']]}
            return res_dict
        else:
            return {}

    def get_grade_raw(self, year, term):
        """获取正方教务成绩json文件"""
        url = parse.urljoin(self.base_url, 'cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005')
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        elif term == '0':
            term = ''
        else:
            print('Please enter the correct term value！！！ ("0" or "1" or "2")')
            return {}
        data = {
            'xnm': year,  # 学年数
            'xqm': term,  # 学期数，第一学期为3，第二学期为12, 整个学年为空''
            '_search': 'false',
            'nd': int(time.time()*1000),
            'queryModel.showCount': '100',  # 每页最多条数
            'queryModel.currentPage': '1',
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
            'time': '0'  # 查询次数
        }
        res = requests.post(url = url, headers=self.headers, data=data, cookies=self.cookies)
        jres = res.json()
        return jres

    def get_schedule(self, year, term):
        """获取课程表信息"""
        url = parse.urljoin(self.base_url, 'kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151')
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        else:
            print('Please enter the correct term value！！！ ("1" or "2")')
            return {}
        data = {
            'xnm': year,
            'xqm': term
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
        # print(res.text)
        jres = res.json()
        # print(jres)
        res_dict = {
            'name': jres['xsxx']['XM'],
            'studentId': jres['xsxx']['XH'],
            'schoolYear': jres['xsxx']['XNM'],
            'schoolTerm': jres['xsxx']['XQMMC'],
            'normalCourse': [{
                'courseTitle': i['kcmc'],
                'teacher': i['xm'],
                'courseId': i['kch_id'],
                'courseSection': i['jc'],
                'courseWeek': i['zcd'],
                'campus': i['xqmc'],
                'courseRoom': i['cdmc'],
                'className': i['jxbmc'],
                'hoursComposition': i['kcxszc'],
                'weeklyHours': i['zhxs'],
                'totalHours': i['zxs'],
                'credit': i['xf'],
                'classtype': i['kclb'],
                'examtype': i['khfsmc']
            }for i in jres['kbList']],
            'otherCourses': [i['qtkcgs'] for i in jres['sjkList']]}
        return res_dict

    def get_schedule_raw(self, year, term):
        """获取原始正方系统课程表信息json信息"""
        url = parse.urljoin(self.base_url, 'kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151')
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        else:
            print('Please enter the correct term value！！！ ("1" or "2")')
            return {}
        data = {
            'xnm': year,
            'xqm': term
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
        jres = res.json()
        return jres

    def get_exam(self, year, term):
        """获取考试信息"""
        url = parse.urljoin(self.base_url, 'kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105')
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        else:
            print('Please enter the correct term value！！！ ("1" or "2")')
            return {}
        data = {
            'xnm': year,  # 学年数
            'xqm': term,  # 学期数，第一学期为3，第二学期为12
            '_search': 'false',
            'nd': int(time.time() * 1000),
            'queryModel.showCount': '100',  # 每页最多条数
            'queryModel.currentPage': '1',
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
            'time': '0'  # 查询次数
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
        jres = res.json()
        if jres.get('items'):  # 防止数据出错items为空
            res_dict = {
                'name': jres['items'][0]['xm'],
                'studentId': jres['items'][0]['xh'],
                'schoolYear': jres['items'][0]['xnmc'][:4],
                'schoolTerm': jres['items'][0]['xqmmc'],
                'exams': [{
                    'courseTitle': i['kcmc'],
                    'teacher': i['jsxx'],
                    'courseId': i['kch'],
                    'reworkMark': i['cxbj'],
                    'selfeditingMark': i['zxbj'],
                    'examName': i['ksmc'],
                    'paperId': i['sjbh'],
                    'examTime': i['kssj'],
                    'eaxmLocation': i['cdmc'],
                    'campus': i['xqmc']
                } for i in jres['items']]}
            return res_dict
        else:
            return {}
    
    def get_exam_raw(self, year, term):
        """获取正方系统考试信息json"""
        url = parse.urljoin(self.base_url, 'kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105')
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        else:
            print('Please enter the correct term value！！！ ("1" or "2")')
            return {}
        data = {
            'xnm': year,  # 学年数
            'xqm': term,  # 学期数，第一学期为3，第二学期为12
            '_search': 'false',
            'nd': int(time.time() * 1000),
            'queryModel.showCount': '100',  # 每页最多条数
            'queryModel.currentPage': '1',
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
            'time': '0'  # 查询次数
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
        jres = res.json()
        return jres
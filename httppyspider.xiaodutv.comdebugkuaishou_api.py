#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-12-07 12:01:53
# Project: kuaishou_api

from pyspider.libs.base_handler import *
from pyspider.libs import mimod
from pyspider.libs.check import CheckData
import hashlib
import hmac
import base64
import urllib
import datetime
import time,json
import re
check_data = CheckData()



class Handler(BaseHandler):
    crawl_config = {
    }
    
    
    @every(minutes=60)
    def on_start(self):
        api_tpl = 'http://www.kuaishou.com/sitemap/baiduVideo/queryEntity?signature={0}&queryDate={1}&number={2}'
        number = 2000
        for i in range(7,15):
            now = datetime.datetime.now()
            date = now.strftime('%Y%m%d')
            sign = self.calculate_sign(number, date)
            url = api_tpl.format(sign,date, number)
            print url
            self.crawl(url, callback=self.index_page)

    @staticmethod
    def calculate_sign(number, date):
        secret = bytes('ftGSrGcfJry7R73y').encode('utf-8')
        message = bytes('number={0}&queryDate={1}'.format(number, date)).encode('utf-8') 
        signature =urllib.quote( base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest()) )
        return signature
    
    
    @config(age=1)
    def index_page(self, response):
        #print response.text
        d = response.json['data']
        for each in d:
            res = {}            
            res['horizontal_thumnail_url'] = each['thumbnail']
            res['vertical_thumnail_url'] = ''            
            res['duration'] = 0
            res['description'] = ''
            res['title'] = each['title']
            if res['title'] == '':
                m = hashlib.md5()
                m.update(res['horizontal_thumnail_url'])
                sign = m.hexdigest()
                res['title'] = u'标题不存在_'+ sign #each['caption']
            res['author'] = each['userName']
            res['link'] = each['contentUrl'].split('?')[0]
            print res['link']
            #vid = re.findall('postRoll-(.*?).mp4', res['link'])[0]
            #res['link'] = 'http://jsmov2.a.yximgs.com/bs2/newWatermark/{0}_zh_4.mp4'.format(vid)
            #print res['link']
            res['block'] = u'现场'
            res['play_count'] = each['viewCount']
            res['comment_count'] = 0
            res['pub_time'] =  int(time.time())
            res['site'] = 'kuaishouapi2'
            # print json.dumps(res,indent=2)
            result = check_data.check(res)
            if result['num']==0:
                try:
                    logger.info('send to mimod: %s', str(result['dict']))
                    ret, code, resp = mimod.send_to_mimod(result['dict'])
                    print json.dumps(result['dict'],indent=2)
                except Exception as ee:
                    print ee
            else:
                print result['error'] 

 
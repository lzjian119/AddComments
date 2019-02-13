#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-02-13 11:08:18
# Project: temp


import random
from pyspider.libs.base_handler import *
from pyspider.libs import mimod
from pyspider.libs.check import CheckData
from pyspider.libs.dc.dc import dead_detect
from pyspider.libs.daku_spider.common_redis_queue import CommonSet
from pyspider.libs import common
from pyspider.libs import check
from urllib2 import unquote
from pyspider.libs import replydb
from pyspider.libs.create_sign import creat_sign_f64
from Crypto.Cipher import AES, DES


check_data = CheckData()
import time, json, re, hashlib

class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; HUAWEI CAZ-AL10 Build/HUAWEICAZ-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/480 MMWEBSDK/190102 Mobile Safari/537.36 MMWEBID/2601 MicroMessenger/7.0.3.1400(0x27000335) Process/toolsmp NetType/WIFI Language/zh_CN",
            "Cookie": 'rewardsn=; wxuin=771363897; devicetype=android-24; lang=zh_CN; wxtokenkey=777; version=27000335; pass_ticket=95sdTZRIEMwKLdr79lkuVseSvpq6SqC2ZW2CAT3HLKIAeHRqQwWz6oOBAfHWunUk; wap_sid2=CLmo6O8CElxvR2k4WENHR3NUVE1qXzdxLVViajMtQzAwcWQ0YjdkVmFmeWtxRWpCc3pPMDhKUXk1UDdCT2hsRlBYM0JzR0FhZ1MxS2NfTUJucDZLTnpFakhRYk9DT01EQUFBfjDqzI3jBTgNQJVO',
            "Accept-Language": "zh-CN,zh-CN;q=0.9,en-US;q=0.8"
        }
    }

    site = 'wechat'
    url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getvideo&__biz=MzIxNjQ1Mjg1Ng==&f=json&count=10&uin=777&key=777&pass_ticket=95sdTZRIEMwKLdr79lkuVseSvpq6SqC2ZW2CAT3HLKIAeHRqQwWz6oOBAfHWunUk&wxtoken=&appmsg_token=995_baQHrzt1O0uv6uDNOkZzfva4aPC4uI5TZfWE1w~~&x5=0&f=json'
    link_url = 'http://v.qq.com/x/page/{}.html'
    @every(minutes=4 * 60)
    def on_start(self):

        url = Handler.url
        block = u'相声小品'
        self.crawl(url, callback=self.index_page,
                   save={
                       'block': block
                   })

    @config(priority=1)
    def index_page(self, response):
        print(response.text)
        print(json.dumps(response.json, indent=4))
        j_msg_list = response.json['general_msg_list']
        json_msg_list = json.loads(j_msg_list)
        print(json.dumps(json_msg_list, indent=4))
        block = response.save['block']

        for i in json_msg_list['list']:
            for tv_board in i['app_msg_ext_info']['multi_app_msg_item_list']:

                res = {}
                res['title'] = tv_board['title']
                res['horizontal_thumnail_url'] = tv_board['cover'].replace('https', 'http')
                # res['optimized_img_url'] = tv_board['poster']['imageUrl'].replace('https', 'http')
                res['duration'] = 0
                res['description'] = ''
                res['author'] = tv_board['author'].strip()
                res['link'] = Handler.link_url.format(tv_board['vid'])
                res['block'] = block
                res['play_count'] = 0
                res['comment_count'] = 0
                res['pub_time'] = int(time.time())
                res['site'] = Handler.site
                print(res['title'])
                print(res['pub_time'])

                result = check_data.check(res)
                if 'date' in response.save.keys():
                    if result['dict']['pub_time'] < response.save['date']:
                        print(str(result['dict']['pub_time']) + ": too old")
                        continue

                if result['num'] == 0:
                    try:
                        logger.info('send to mimod: %s', str(result['dict']))
                        ret, code, resp = mimod.send_to_mimod(result['dict'])
                        print(json.dumps(result['dict'], indent=2))
                    except Exception as ee:
                        print(ee)
                else:
                    print(result['error'])

            tv_board = i['app_msg_ext_info']
            res = {}
            res['title'] = tv_board['title']
            res['horizontal_thumnail_url'] = tv_board['cover'].replace('https', 'http')
            # res['optimized_img_url'] = tv_board['poster']['imageUrl'].replace('https', 'http')
            # res['duration'] = tv_board['duration']
            res['duration'] = 0
            res['description'] = ''
            res['author'] = tv_board['author'].strip()
            res['link'] = Handler.link_url.format(tv_board['vid'])
            res['block'] = block
            res['play_count'] = 0
            res['comment_count'] = 0
            res['pub_time'] = int(time.time())
            res['site'] = Handler.site
            print(res['title'])
            print(res['pub_time'])

            result = check_data.check(res)
            if 'date' in response.save.keys():
                if result['dict']['pub_time'] < response.save['date']:
                    print(str(result['dict']['pub_time']) + ": too old")
                    continue

            if result['num'] == 0:
                try:
                    logger.info('send to mimod: %s', str(result['dict']))
                    ret, code, resp = mimod.send_to_mimod(result['dict'])
                    print(json.dumps(result['dict'], indent=2))
                except Exception as ee:
                    print(ee)
            else:
                print(result['error'])

        # 还有视频时can_msg_continue等于1
        if response.json['can_msg_continue'] == 1:
            url = Handler.url
            url += '&offset=' + str(response.json['next_offset'])
            self.crawl(url, callback=self.index_page,
                       save={
                           'block': block
                       })











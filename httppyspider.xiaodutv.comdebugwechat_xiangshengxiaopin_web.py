#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-02-14 08:24:08
# Project: wechat_xiangshengxiaopin_web

import time, json, re, hashlib
import random
from urllib2 import unquote

from pyspider.libs.base_handler import *
from pyspider.libs import mimod
from pyspider.libs.check import CheckData
from pyspider.libs.dc.dc import dead_detect
from pyspider.libs.daku_spider.common_redis_queue import CommonSet
from pyspider.libs import common
from pyspider.libs import check
from pyspider.libs import replydb
from pyspider.libs.create_sign import creat_sign_f64

'''
通过搜狗搜索,web端抓取最新更新的十期作品
只能抓取最新的十期,不能抓取所有
'''

check_data = CheckData()


class Handler(BaseHandler):

    crawl_config = {
        'proxy': '192.168.80.59:8889',
        # 'proxy': '82.147.116.201:41234',
        # 'proxy': '213.32.252.120:45728',
        'headers': {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6821.400 QQBrowser/10.3.3040.400",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
    }

    # 公众号信息
    public_accounts_info = [
        {'account': 'bx5966', 'name': u'欢乐小品', 'block': u'相声小品'},
        {}
    ]
    site = 'wechat'
    url_link = 'http://v.qq.com/x/page/{}.html'

    @every(minutes=4 * 60)
    def on_start(self):

        for i in Handler.public_accounts_info:
            if not i:
                continue

            account = i['account']
            block = i['block']
            name = i['name']
            url_open = 'http://weixin.sogou.com/weixin?type=1&query=%s&ie=utf8&_sug_=n&_sug_type_= ' % (account, )

            self.crawl(url_open,
                       callback=self.index_page,
                       save={
                           'block': block,
                           'account': account,
                           'name': name
                       })

    @config(age=1)
    def index_page(self, response):
        print(response.text)
        doc = response.doc
        save = response.save
        block = save['block']
        account = save['account']
        name = save['name']

        for i in doc('ul[class="news-list2"]')('div[class="gzh-box2"]').items():
            # print(i)
            txt_box = i('div[class="txt-box"]')
            wx_account = txt_box('p[class="info"]')('label').text()
            # print(wx_account + '---' + account)
            if wx_account != account:
                continue

            url = txt_box('p[class="tit"]')('a').attr.href
            print(url)
            self.crawl(url,
                       callback=self.detail_page,
                       save={
                           'block': block,
                           'account': account,
                           'name': name
                       })

    def detail_page(self, response):
        # print(response.text)

        tt = r'msgList = '
        patt = tt +r'.*?};'
        result = re.findall(patt, response.doc.html())
        if not result:
            print(response.text)
            return

        print(result[0])
        str_target = result[0][len(tt):-1]
        print(str_target)
        save = response.save
        block = save['block']

        j = json.loads(str_target)
        for i in j['list']:
            msg_info = i['app_msg_ext_info']
            res = Handler.set_res(msg_info, save, block)
            host = 'http://mp.weixin.qq.com'
            if res:
                url = host + msg_info['content_url']
                url = url.replace('&amp;amp;', '&')
                url = url.replace('&amp;', '&')
                print(url)
                self.crawl(url,
                           callback=self.vid_page,
                           save={
                                'res': res
                           })

            for each in msg_info['multi_app_msg_item_list']:
                res = Handler.set_res(each, save, block)
                if res:
                    url = host + each['content_url']
                    url = url.replace('&amp;amp;', '&')
                    url = url.replace('&amp;', '&')
                    print(url)
                    self.crawl(url,
                               callback=self.vid_page,
                               save={
                                    'res': res
                               })

    def vid_page(self, response):
        # print(response.text)
        save = response.save
        res = save['res']
        doc = response.doc

        # iframe_data = doc('div[class="rich_media_content "]')('p')('iframe')
        iframe_data = doc('div[id="js_content"]')('p')('iframe')
        # print(iframe_data)
        data_src = iframe_data.attr['data-src']
        # print(data_src)

        vid = re.findall('vid=.*', data_src)
        vid = vid[0][4:]
        res['link'] = Handler.url_link.format(vid)
        print(res['link'])

        result = check_data.check(res)
        if 'date' in save.keys():
            if result['dict']['pub_time'] < save['date']:
                print(str(result['dict']['pub_time']) + ": too old")
                return

        if result['num'] == 0:
            try:
                logger.info('send to mimod: %s', str(result['dict']))
                ret, code, resp = mimod.send_to_mimod(result['dict'])
                print(json.dumps(result['dict'], indent=2))
            except Exception as ee:
                print(ee)
        else:
            print(result['error'])

    @staticmethod
    def set_res(json_data, save, block):
        res = {}
        res['title'] = json_data['title']
        res['horizontal_thumnail_url'] = json_data['cover'].replace('https', 'http')
        # res['optimized_img_url'] = tv_board['poster']['imageUrl'].replace('https', 'http')
        # res['duration'] = tv_board['duration']
        res['duration'] = 0
        res['description'] = ''
        res['author'] = save['name']
        res['link'] = ''
        res['block'] = block
        res['play_count'] = 0
        res['comment_count'] = 0
        res['pub_time'] = int(time.time())
        res['site'] = Handler.site
        print(res['title'])
        print(res['pub_time'])

        return res











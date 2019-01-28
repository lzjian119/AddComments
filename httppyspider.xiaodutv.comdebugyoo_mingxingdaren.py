#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-01-23 17:46:38
# Project: yoo_mingxingdaren

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

check_data = CheckData()
import time, json, re, hashlib

url_dict = [
    ['http://hgaccess.video.qq.com/huoguo/user_work_list?vappid=49109510&vsecret=c1202d7f3ba41f86cdd2d3d1082605b4ed764c21e29520f3&callback=func&raw=1',
     # {"account": {"id": "6019961", "type": 50},"pageContext": "{\"offset\":%d,\"page_size\":20,\"time\":1548222864,\"last_node_id\":\"\",\"last_node_score\":2147483647,\"top_vid_set\":[]}","countReg": True},
     '6019961',
     'ver_img'] # Hello娱乐  竖图
]

class Handler(BaseHandler):
    crawl_config = {
        'iteg': time.time()
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset:UTF-8',
        # 'Cookie': 'RK=mn+2yjyfSq; eas_sid=B1t5v1G7m820X0v1F415u9b7G4; pgv_pvi=4031234048; tvfe_boss_uuid=829cdb90dbce02eb; pac_uid=1_1123469970; o_cookie=1123469970; ptcz=e0e44363e16b6d0cfb84657aeebc5111411f820cb194b633ad959ff8b3792f35; pt2gguin=o1123469970; pgv_pvid=2548788446',
        # 'Accept-Language': 'zh-CN,zh;q=0.8',
        # 'Referer': 'http://yoo.qq.com/m/person.html?userid=6019961&share_uin=0&ptag=huoguo&hgptag=huoguo'
    }
    common_set = CommonSet("qq_comment")
    site = 'yooqq'
    block = u'明星达人'
    count_per_page = 20

    @every(minutes=4 * 60)
    def on_start(self):
        # data = '{"account":{"id":"6019961","type":50},"pageContext":"{\"offset\":20,\"page_size\":20,\"time\":1548222864,\"last_node_id\":\"\",\"last_node_score\":2147483647,\"top_vid_set\":[]}","countReg":true}'

        for i in url_dict:
            url = i[0]
            data = Handler.get_url_data(i[1])

            # print(data)
            self.crawl(url,
                       headers=Handler.headers,
                       method='POST',
                       data=json.dumps(data),
                       save={'block':Handler.block, 'ver_img': i[2], 'link': url, 'account_id': i[1], 'first': 1},
                       callback=self.index_page)

    @config(age=1)
    def index_page(self, response):

        # print json.dumps(response.json, indent=2)

        j = response.json
        if j['msg'] != 'ok.':
            print j['msg']

        j_data = j['data']

        # print content.replace(replace,u'')[:-1]
        # j = json.loads(response.content.decode('utf-8').replace(replace1, "")[:-1])
        # j = json.loads(response.content.decode('utf-8')[:-1])
        if "collections" not in j_data.keys() or j_data['collections'] is None:
            return

        block = response.save['block']
        link = response.save['link']
        account_id = response.save['account_id']
        first = response.save['first']
        ver_img = response.save['ver_img']

        print("count=" + str(len(j_data['collections'])))
        for each in j_data['collections']:
            tv_board = each['tvBoard']
            res = {}
            res['title'] = tv_board['videoData']['title']
            res['horizontal_thumnail_url'] = tv_board['poster']['imageUrl'].replace('https', 'http')
            #res['optimized_img_url'] = tv_board['poster']['imageUrl'].replace('https', 'http')
            res['duration'] = tv_board['duration']
            res['description'] = ''
            res['author'] = tv_board['user']['userInfo']['userName'].strip()
            res['link'] = tv_board['shareItem']['shareUrl'].replace('https', 'http')
            res['block'] = block
            res['play_count'] = tv_board['poster']['playCountL']
            res['comment_count'] = tv_board['commentInfo']['commentCount']
            res['pub_time'] = tv_board['timeStamp']
            res['site'] = Handler.site
            print(res['title'])
            print(res['pub_time'])
            result = check_data.check(res)
            if 'date' in response.save.keys():
                 if result['dict']['pub_time'] < response.save['date']:
                     print str(result['dict']['pub_time']) + ": too old"
                     continue

            if result['num'] == 0:
                try:
                    logger.info('send to mimod: %s', str(result['dict']))
                    ret, code, resp = mimod.send_to_mimod(result['dict'])
                    print json.dumps(result['dict'], indent=2)
                    # vid = re.findall(r'/([^./]+?)\.html', res['link'])[0]
                    # print(vid)
                except Exception as ee:
                    print ee
            else:
                print result['error']

        # 获取更多
        total_count = j_data['count']
        print(total_count)
        if total_count > Handler.count_per_page and first == 1:
            for i in range(Handler.count_per_page,total_count,Handler.count_per_page):
                url = link + '#' + str(i)
                data = Handler.get_url_data(account_id, offset=i)
                self.crawl(url,
                           headers=Handler.headers,
                           method='POST',
                           data=json.dumps(data),
                           save={'block': Handler.block, 'ver_img': ver_img, 'link': url, 'account_id': account_id, 'first': 0},
                           callback=self.index_page)

    @staticmethod
    def get_url_data(account_id, **kwargs):

        if not account_id or not isinstance(account_id, six.string_types):
            return {}

        offset = 0
        if kwargs:
            if kwargs.get('offset') and isinstance(kwargs.get('offset'), six.integer_types):
                offset = kwargs['offset']

        data = {"account": {"id": account_id, "type": 50},
         "pageContext": "{\"offset\":"+str(offset)+",\"page_size\":"+str(Handler.count_per_page)+",\"time\":1548222864,\"last_node_id\":\"\",\"last_node_score\":2147483647,\"top_vid_set\":[]}",
         "countReg": True}

        return data


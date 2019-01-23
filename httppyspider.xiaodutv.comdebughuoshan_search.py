#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-10-30 11:30:48
# Project: huoshan_search

from pyspider.libs.base_handler import *
from pyspider.libs.check import CheckData
from pyspider.libs.create_sign import creat_sign_f64
from pyspider.libs.daku_spider.common_redis_queue import CommonSet
from pyspider.libs import replydb
from pyspider.libs import mimod
from pyspider.libs import utils

import hashlib, random, json, re
import time

check_data = CheckData()


def md5_str(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


class Handler(BaseHandler):
    crawl_config = {
    }

    common_set = CommonSet("huoshan")
    site = 'huoshan'

    @every(minutes=6 * 60)
    def on_start(self):
        url_list = [
            # [
            #     u'https://hotsoon.snssdk.com/hotsoon/general_search/?query=唱歌&user_action=Initiative&offset={}&count=10&search_type=2&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540871602733&ab_version=391711%2C564003%2C570935%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C557631%2C404280%2C568545%2C570099%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C571139%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C457535%2C523976%2C571445%2C550979&ts=1540871602&as=a2a58dbd423bdbd5474355&cp=dab9be522973dd53e2MyUc&mas=0063f8292442325352792e8eb7222a9b52c6ee26ea06686ea1',
            #     u'唱歌达人',
            #     u'搜索唱歌视频'],
            # [
            #     u'https://hotsoon.snssdk.com/hotsoon/general_search/?query=搞笑视频&user_action=Initiative&offset={}&count=10&search_type=2&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540871602733&ab_version=391711%2C564003%2C570935%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C557631%2C404280%2C568545%2C570099%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C571139%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C457535%2C523976%2C571445%2C550979&ts=1540871602&as=a2a58dbd423bdbd5474355&cp=dab9be522973dd53e2MyUc&mas=0063f8292442325352792e8eb7222a9b52c6ee26ea06686ea1',
            #     u'搞笑达人',
            #     ],
            [
                u'https://hotsoon.snssdk.com/hotsoon/general_search/?query=唱歌&count=10&user_action=Initiative&offset={}&search_type=0&live_sdk_version=550&iid=58171584612&device_id=61638140601&ac=wifi&channel=huawei&aid=1112&app_name=live_stream&version_code=550&version_name=5.5.0&device_platform=android&ssmix=a&device_type=HUAWEI+CAZ-AL10&device_brand=HUAWEI&language=zh&os_api=24&os_version=7.0&openudid=d77f81aa505cf9d1&manifest_version_code=550&resolution=1080*1788&dpi=480&update_version_code=5505',
                u'唱歌达人',
                u'搜索唱歌视频'
            ],
            [
                u'https://hotsoon.snssdk.com/hotsoon/general_search/?query=搞笑视频&count=10&user_action=Initiative&offset={}&search_type=0&live_sdk_version=550&iid=58171584612&device_id=61638140601&ac=wifi&channel=huawei&aid=1112&app_name=live_stream&version_code=550&version_name=5.5.0&device_platform=android&ssmix=a&device_type=HUAWEI+CAZ-AL10&device_brand=HUAWEI&language=zh&os_api=24&os_version=7.0&openudid=d77f81aa505cf9d1&manifest_version_code=550&resolution=1080*1788&dpi=480&update_version_code=5505',
                u'搞笑达人',
            ]
        ]
        for lt in url_list:
            print lt
            url = lt[0]
            block = lt[1]
            for num in range(100):  #1000改为100，太多被封
                crawl_url=url.format(num*10)
                self.crawl(crawl_url,
                           save=block,
                           params={
                               '_rticket': 1548204782560,
                               'ts': 1548204782,
                               'mas': '0065824a6bf9d06af6c56f27ddc2886e9e4c2c20cac40408f6',
                               'as': 'a2a5ab04fede4c4a270033&cp=b1ecc659e37147aae2MmUq',
                               'ab_version': '709965%2C712301%2C708558%2C662547%2C691945%2C712776%2C689908%2C505466%2C699188%2C692223%2C706102%2C707561%2C612163%2C710301%2C557631%2C678007%2C674738%2C653181%2C701412%2C679568%2C680404%2C661943%2C384499%2C374107%2C705072%2C633217%2C709961%2C682009%2C665355%2C709820%2C710143%2C679987%2C643985%2C704997%2C299908%2C508755%2C659570%2C711049%2C712086%2C598627%2C457534%2C641185%2C712695%2C703436'},
                           callback=self.index_page)

    @config(age=10)
    def index_page(self, response):

        block = response.save
        j_dict = response.json
        # print(json.dumps(response.json, indent=4))

        try:
            # j_data = j_dict['data'][0]
            j_data = {}
            for i in j_dict['data']:
                if i.get('item_result'):
                    j_data = i
                    break
            if j_data == {}:
                print(json.dumps(response.json, indent=4))
                return

        except KeyError:
            print(json.dumps(response.json, indent=4))
            return
        site = self.site
        insert_arr = []
        for each in j_data['item_result']['items']:
            res = {}

            # print json.dumps(each, indent=4)

            play_url = each['item']['video']['url_list'][0]
            res['link'] = re.sub('&ts=\d{10}', '', play_url)
            res['title'] = each['item']['title']
            if len(res['title']) < 1:
                res['title'] = "标题不存在_{}".format(md5_str(res['link']))
            if each['item']['video']['duration']:
                res['duration'] = int(float(each['item']['video']['duration']))
            res['vertical_thumnail_url'] = ''
            res['horizontal_thumnail_url'] = each['item']['video']["cover"]["url_list"][0].replace('.webp', '')
            res['description'] = ''
            res['author'] = each['item']["author"]["id"]

            res['block'] = block
            res['site'] = site
            res['play_count'] = "0"
            res['comment_count'] = each['item']['stats']['comment_count']
            res['pub_time'] = each['item']["create_time"]

            result = check_data.check(res)
            if result['num'] == 0:
                try:
                    logger.info('send to mimod: %s', str(result['dict']))
                    if utils.check_image(res['horizontal_thumnail_url']) == 1:
                        print 111111
                        ret, code, resp = mimod.send_to_mimod(result['dict'])
                        print "=========== SEND ==========="
                        print json.dumps(result['dict'], indent=4)

                    # 抓取评论
                    if res['comment_count'] > 200:
                        for i in range(0, 200, 20):
                            # url = 'https://hotsoon.snssdk.com/hotsoon/item/%s/comments/?offset=%d&count=20' % (each['data']['id_str'],i)
                            url = "https://hotsoon.snssdk.com/hotsoon/item/%s/comments/?offset=%d&count=20&live_sdk_version=280&iid=17973913310&device_id=29535583655&ac=wifi&channel=tengxun&aid=1112&app_name=live_stream&version_code=280&version_name=2.8.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&os_api=23&os_version=6.0.1&uuid=359320050951630&openudid=c4d0375ebc82b961&manifest_version_code=280&resolution=1440*2392&dpi=560&update_version_code=2802&ts=%d&as=a235e5018df48a2fc2&cp=574fa65adc271cf0e2" % (
                                each['item']['id_str'], i, int(time.time()))
                            self.crawl(url,
                                       callback=self.detail_page,
                                       save={'link': res['link'], 'block': block})
                    else:
                        print "00000"
                        pn = res['comment_count'] / 20 + 1
                        for i in range(0, pn, 20):
                            # url = 'https://hotsoon.snssdk.com/hotsoon/item/%s/comments/?offset=%d&count=20' % (each['data']['id_str'],i)
                            url = "https://hotsoon.snssdk.com/hotsoon/item/%s/comments/?offset=%d&count=20&live_sdk_version=280&iid=17973913310&device_id=29535583655&ac=wifi&channel=tengxun&aid=1112&app_name=live_stream&version_code=280&version_name=2.8.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&os_api=23&os_version=6.0.1&uuid=359320050951630&openudid=c4d0375ebc82b961&manifest_version_code=280&resolution=1440*2392&dpi=560&update_version_code=2802&ts=%d&as=a235e5018df48a2fc2&cp=574fa65adc271cf0e2" % (
                                each['item']['id_str'], i, int(time.time()))
                            print"999999:", url
                            self.crawl(url,
                                       callback=self.detail_page,
                                       save={'link': res['link'], 'block': block})
                except Exception as ee:
                    print ee
            else:
                print result['error']

    @config(priority=2)
    def detail_page(self, response):
        comments = response.json['data']['comments']
        block = response.save['block']
        for comment in comments:
            comment_dict = {}
            link_sign1, link_sign2 = creat_sign_f64(response.save['link'])
            comment_dict['link_sign1'] = link_sign1
            comment_dict['link_sign2'] = link_sign2
            comment_dict['worksname'] = block
            name = re.sub(r'<.*?>', '', comment['user']['nickname'])
            name = re.sub(r'<.*|.*>', '', name)
            comment_dict['uname'] = name
            print name
            comment_dict['uicon'] = name
            comment_dict['pubtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            # print comment_dict['pubtime']
            comment_dict['cs'] = self.site
            comment = re.sub(r'<.*>', '', comment['text'])
            comment_dict['info'] = re.sub(r'<.*|.*>', '', comment)
            # print comment
            print comment_dict['info']
            if len(comment_dict['info']) > 30:
                continue
            print comment_dict
            md5_string = response.save['link'] + name + comment_dict['info']
            cid = hashlib.md5(md5_string.encode('utf-8')).hexdigest()
            if self.common_set.ismember(cid):
                pass
            else:
                self.common_set.add(cid)
                try:
                    insert_db = replydb.REPLYDB()
                    link_id = insert_db._insert(tablename='wise_video_reply_shortvideo_0', **comment_dict)
                    print json.dumps(comment_dict, indent=2)
                except Exception as ee:
                    print ee






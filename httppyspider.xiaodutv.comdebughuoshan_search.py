#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-10-30 11:30:48
# Project: huoshan_search

from pyspider.libs.base_handler import *
from pyspider.libs.check import CheckData
from pyspider.libs.daku_spider.common_redis_queue import CommonSet
from pyspider.libs import mimod
from pyspider.libs import utils

import hashlib,random,json,re

check_data = CheckData()


def md5_str(str):
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()



class Handler(BaseHandler):
    crawl_config = {
        'headers':{'User-Agent': 'com.ss.android.ugc.live/490 (Linux; U; Android 8.1.0; zh_CN; MI 8 SE; Build/OPM1.171019.019; Cronet/58.0.2991.0)'}
    }
    
    common_set = CommonSet("huoshan")
    site='huoshan'
    @every(minutes=6 * 60)
    def on_start(self):
        url_list=[
            [u'https://api.huoshan.com/hotsoon/general_search/?query=唱歌&user_action=Initiative&offset={}&count=10&search_type=2&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540871602733&ab_version=391711%2C564003%2C570935%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C557631%2C404280%2C568545%2C570099%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C571139%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C457535%2C523976%2C571445%2C550979&ts=1540871602&as=a2a58dbd423bdbd5474355&cp=dab9be522973dd53e2MyUc&mas=0063f8292442325352792e8eb7222a9b52c6ee26ea06686ea1',
            u'唱歌达人',
            u'搜索唱歌视频'],
            [u'https://api.huoshan.com/hotsoon/general_search/?query=搞笑视频&user_action=Initiative&offset={}&count=10&search_type=2&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540871602733&ab_version=391711%2C564003%2C570935%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C557631%2C404280%2C568545%2C570099%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C571139%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C457535%2C523976%2C571445%2C550979&ts=1540871602&as=a2a58dbd423bdbd5474355&cp=dab9be522973dd53e2MyUc&mas=0063f8292442325352792e8eb7222a9b52c6ee26ea06686ea1',
             u'搞笑达人',
            ]
    ]
        for lt in url_list:
            print lt
            url=lt[0]
            block=lt[1]
            for num in range(100):  #1000改为100，太多被封
                crawl_url=url.format(num*10)
                self.crawl(crawl_url,save=block,callback=self.index_page)

    @config(age=10)
    def index_page(self, response):
        block=response.save
        j_dict=response.json
        try:
            j_data=j_dict['data'][0]
        except KeyError:
            return
        site=self.site
        insert_arr = []
        for each in j_data['item_result']['items']:
            res={}
            play_url=each['item']['video']['url_list'][0]
            res['link']=re.sub('&ts=\d{10}','',play_url)
            res['title']=each['item']['title']
            if len(res['title']) < 1:
                res['title'] = "标题不存在_{}".format(md5_str(res['link']))
            if each['item']['video']['duration']:
                res['duration']=int(float(each['item']['video']['duration']))
            res['vertical_thumnail_url'] = ''
            res['horizontal_thumnail_url'] =each['item']['video']["cover"]["url_list"][0].replace('.webp','') 
            res['description'] = ''
            res['author'] = each['item']["author"]["id"]
            
            res['block'] = block
            res['site'] = site
            res['play_count'] = "0"
            res['comment_count'] = 0
            res['pub_time'] = each['item']["create_time"]
            
            


            result = check_data.check(res)      
            if result['num']==0:
                try:
                    logger.info('send to mimod: %s', str(result['dict']))
                    if utils.check_image(res['horizontal_thumnail_url']) == 1:
                        print 111111
                        ret, code, resp = mimod.send_to_mimod(result['dict'])
                        print "=========== SEND ==========="
                        print json.dumps(result['dict'],indent=4)
                except Exception as ee:
                    print ee
            else:
                print result['error']

    
    
    
    
    
    
    
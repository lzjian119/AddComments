#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-21 11:38:49
# Project: xigua_app

from pyspider.libs.base_handler import *
from pyspider.libs import mimod
from pyspider.libs.check import CheckData
from pyspider.libs.dc.dc import dead_detect
from pyspider.libs.create_sign import creat_sign_f64
from pyspider.libs.daku_spider.common_redis_queue import CommonSet
from pyspider.libs import replydb
from pyspider.libs import common

check_data = CheckData()
import time, json, re
import hashlib
import random


class Handler(BaseHandler):
    crawl_config = {
        "itag": 2
    }
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; Letv X500 Build/DBXCNOP5902812084S) VideoArticle/6.5.3 okhttp/3.7.0.6',
        'Host': 'is.snssdk.com',
    }
    headers2 = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 6 Build/MMB29K) VideoArticle/6.5.3 okhttp/3.7.0.6',
        'Host': 'it.snssdk.com'
    }
    cookies = {
        'Cookie': 'install_id=33309910436; ttreq=1$ab8130828882ff7064e8aa8bfa088dc4b92039c3; odin_tt=a255657cc487266cf1a810c4fa29d674898075f102d013203c488c08f6c29d0711e163ffde4d682a1bb53f5abcaac80d; qh[360]=1; alert_coverage=74'
    }
    urls = {
        # "http://is.snssdk.com/video/app/stream/v51/?category=subv_xg_movie&refer=1&count=20&min_behot_time=%d&list_entrance=main_tab&last_refresh_sub_entrance_interval=%d&loc_mode=6&tt_from=refresh_auto&lac=41208&cid=8944317&play_param=codec_type%%3A1&iid=33309910436&device_id=52743256472&ac=wifi&channel=tianzhuo_xg_sg&aid=32&app_name=video_article&version_code=653&version_name=6.5.3&device_platform=android&ab_version=349010%%2C344692%%2C353537%%2C356327%%2C324397%%2C357803%%2C358092%%2C358365%%2C346902%%2C356603%%2C350431%%2C355629%%2C354440%%2C325214%%2C354608%%2C355548%%2C346576%%2C348803%%2C320650&ssmix=a&device_type=Letv+X500&device_brand=Letv&language=zh&os_api=23&os_version=6.0&uuid=869611023501525&openudid=f3eb301815e5d459&manifest_version_code=253&resolution=1080*1920&dpi=420&update_version_code=65307&_rticket=%d&fp=RrT_FlGIFWGSFlcOFlU1FYweFW4M&rom_version=eui_5.9.028s_DBXCNOP5902812084S":"影视片段",
        # "https://ic.snssdk.com/video/app/stream/v51/?category=subv_video_health&refer=1&count=20&max_behot_time=%d&list_entrance=main_tab&last_refresh_sub_entrance_interval=%d&loc_mode=0&tt_from=load_more&iid=28488328953&device_id=29535583655&ac=wifi&channel=store_tengxun_wzl&aid=32&app_name=video_article&version_code=644&version_name=6.4.4&device_platform=android&ab_version=300070%%2C300421%%2C236847%%2C246275%%2C299255%%2C301210%%2C299928%%2C295065%%2C297666%%2C252881%%2C240348%%2C298312%%2C257292%%2C297111%%2C300246%%2C293532%%2C295676%%2C299937%%2C299211%%2C295607&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&uuid=359320050951630&openudid=c4d0375ebc82b961&manifest_version_code=244&resolution=1440*2392&dpi=560&update_version_code=64408&_rticket=%d&fp=4lTqFSUOLlG7FlGSFlU1FYFSc2mb":"养生",
        "http://is.snssdk.com/video/app/stream/v51/?category=subv_xg_life&refer=1&count=20&max_behot_time=%d&list_entrance=main_tab&last_refresh_sub_entrance_interval=%d&loc_mode=6&tt_from=refresh_auto&lac=41208&cid=8944317&play_param=codec_type%%3A1&iid=33309910436&device_id=52743256472&ac=wifi&channel=tianzhuo_xg_sg&aid=32&app_name=video_article&version_code=653&version_name=6.5.3&device_platform=android&ab_version=349010%%2C344692%%2C353537%%2C356327%%2C324397%%2C357803%%2C358092%%2C358365%%2C346902%%2C356603%%2C350431%%2C355629%%2C354440%%2C325214%%2C354608%%2C355548%%2C346576%%2C348803%%2C320650&ssmix=a&device_type=Letv+X500&device_brand=Letv&language=zh&os_api=23&os_version=6.0&uuid=869611023501525&openudid=f3eb301815e5d459&manifest_version_code=253&resolution=1080*1920&dpi=420&update_version_code=65307&_rticket=%d&fp=RrT_FlGIFWGSFlcOFlU1FYweFW4M&rom_version=eui_5.9.028s_DBXCNOP5902812084S": "生活",
        "http://is.snssdk.com/video/app/stream/v51/?category=subv_video_food&refer=1&count=20&max_behot_time=%d&list_entrance=main_tab&last_refresh_sub_entrance_interval=%d&loc_mode=6&tt_from=load_more&lac=41208&cid=8944317&play_param=codec_type%%3A1&iid=33309910436&device_id=52743256472&ac=wifi&channel=tianzhuo_xg_sg&aid=32&app_name=video_article&version_code=653&version_name=6.5.3&device_platform=android&ab_version=349010%%2C344692%%2C353537%%2C356327%%2C324397%%2C357803%%2C358092%%2C358365%%2C346902%%2C356603%%2C350431%%2C355629%%2C354440%%2C325214%%2C354608%%2C355548%%2C346576%%2C348803%%2C320650&ssmix=a&device_type=Letv+X500&device_brand=Letv&language=zh&os_api=23&os_version=6.0&uuid=869611023501525&openudid=f3eb301815e5d459&manifest_version_code=253&resolution=1080*1920&dpi=420&update_version_code=65307&_rticket=%d&fp=RrT_FlGIFWGSFlcOFlU1FYweFW4M&rom_version=eui_5.9.028s_DBXCNOP5902812084S": "美食"

    }
    url2 = {
        # "https://is.snssdk.com/video/app/stream/v51/?category=subv_xg_movie&refer=1&count=20&max_behot_time=%d&list_entrance=main_tab&last_refresh_sub_entrance_interval=%d&loc_mode=0&tt_from=refresh_auto&lac=41208&cid=8944317&play_param=codec_type%%3A1&iid=33309247789&device_id=29535583655&ac=wifi&channel=tengxun_new&aid=32&app_name=video_article&version_code=653&version_name=6.5.3&device_platform=android&ab_version=349009%%2C344692%%2C321290%%2C356347%%2C350722%%2C358091%%2C354867%%2C240348%%2C358362%%2C356603%%2C354439%%2C325213%%2C346576%%2C320650&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&uuid=359320050951630&openudid=c4d0375ebc82b961&manifest_version_code=253&resolution=1440*2392&dpi=560&update_version_code=65307&_rticket=%d&fp=4lTqFSUOLlG7FlGSFlU1FYFSc2mb&rom_version=MMB29K":"影视片段",

        "https://is.snssdk.com/video/app/stream/v51/?category=subv_video_food&refer=1&count=20&min_behot_time=%d&list_entrance=main_tab&last_refresh_sub_entrance_interval=%d&loc_mode=0&lac=41208&cid=8944317&play_param=codec_type%%3A1&iid=33309247789&device_id=29535583655&ac=wifi&channel=tengxun_new&aid=32&app_name=video_article&version_code=653&version_name=6.5.3&device_platform=android&ab_version=349009%%2C344692%%2C321290%%2C356347%%2C350722%%2C358091%%2C354867%%2C240348%%2C358362%%2C356603%%2C354439%%2C325213%%2C346576%%2C320650&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&uuid=359320050951630&openudid=c4d0375ebc82b961&manifest_version_code=253&resolution=1440*2392&dpi=560&update_version_code=65307&_rticket=%d&fp=4lTqFSUOLlG7FlGSFlU1FYFSc2mb&rom_version=MMB29K": "美食"
    }

    common_set = CommonSet("toutiao")
    site = 'toutiao'

    @every(minutes=3 * 1)
    def on_start(self):
        for k, v in self.urls.items():
            url = k % (int(time.time()) - 4 * 60, int(time.time()), int(time.time() * 1000))
            block = v
            self.crawl(url, headers=self.headers, cookies=self.cookies, save={"block": block}, callback=self.index_page)

    @config(age=1)
    def index_page(self, response):
        data = response.json
        # print data
        data = data["data"]
        item = response.save
        block = item["block"]
        print data
        for each in range(len(data)):

            content = data[each]["content"]
            content_1 = json.loads(content)
            res = {}
            if "video_play_info" not in content_1:
                print "pass"
                continue
            image = content_1["video_play_info"]
            img = json.loads(image)
            res['horizontal_thumnail_url'] = img["poster_url"]
            print res['horizontal_thumnail_url']

            res['vertical_thumnail_url'] = ''
            res['duration'] = content_1["video_duration"]
            res['description'] = content_1["abstract"]
            print res['description']
            res['title'] = content_1["title"]
            print res['title']
            if res['title'] == '':
                m = hashlib.md5()
                m.update(res['horizontal_thumnail_url'])
                sign = m.hexdigest()
                res['title'] = u'标题不存在_' + sign
            res['author'] = content_1["source"]
            print res['author']
            res['link'] = content_1["article_url"].replace("https", "http")
            res['block'] = block
            res['play_count'] = content_1["read_count"]
            res['comment_count'] = content_1["comment_count"]
            res['pub_time'] = content_1["publish_time"]
            res['site'] = self.site
            # res["keywords"]=content_1["keywords"]
            # print res["keywords"]
            # print json.dumps(res,indent=2)
            result = check_data.check(res)
            if result['num'] == 0:
                try:
                    logger.info('send to mimod: %s', str(result['dict']))
                    ret, code, resp = mimod.send_to_mimod(result['dict'])
                    print json.dumps(result['dict'], indent=2)

                    # 抓取评论
                    group_id = content_1['group_id']
                    item_id = content_1['item_id']
                    comment_count = res['comment_count']
                    comment_count_crawl = min(comment_count, 200)

                    for i in range(0, comment_count_crawl, 20):
                        url = 'https://ic.snssdk.com/article/v2/tab_comments/?aggr_type=1&count=20&tab_index=0&iid=57860049749&device_id=61638140601&ac=wifi&channel=huawei&aid=32&app_name=video_article&version_code=728&version_name=7.2.8&device_platform=android&os_api=24&os_version=7.0&uuid=863531037335924&openudid=d77f81aa505cf9d1&manifest_version_code=328&resolution=1080*1788&dpi=480&update_version_code=72806&_rticket=1547625813202&fp=i2TrFSLMFSZ7FlGWFSU1F2FeJzTq&rom_version=EmotionUI_5.0.4_CAZ-AL10C00B387&ts=1547625813'
                        url += '&offset=%d&group_id=%s&item_id=%s' % (i, group_id, item_id)
                        self.crawl(url, headers=self.headers, cookies=self.cookies, callback=self.detail_page,
                                   save={
                                       'block': block,
                                       'link': url
                                   })

                except Exception as ee:
                    print ee
            else:
                print result['error']

    @config(priority=2)
    def detail_page(self, response):
        print(json.dumps(response.json, indent=4))

        j = response.json
        if j['message'] != 'success':
            print j['message']
            return

        block = response.save['block']
        link = response.save['link']
        for each0 in j['data']:
            each = each0['comment']
            comment_dict = {}
            link_sign1, link_sign2 = creat_sign_f64(link)
            comment_dict['link_sign1'] = link_sign1
            comment_dict['link_sign2'] = link_sign2
            comment_dict['worksname'] = block
            comment_dict['uname'] = each['user_name'].replace('\n', '').strip()
            comment_dict['uicon'] = each['user_profile_image_url'].replace('\n', '').strip()
            comment_dict['pubtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            comment_dict['cs'] = self.site
            comment_dict['info'] = each['text'].replace('\n', '').strip()

            comment_len = len(comment_dict['info'])
            if comment_len > 30 or comment_len == 0:
                continue

            md5_string = link + comment_dict['uname'] + comment_dict['info']
            cid = hashlib.md5(md5_string.encode('utf-8')).hexdigest()
            if self.common_set.ismember(cid):
                pass
            else:
                self.common_set.add(cid)
                try:
                    insert_db = replydb.REPLYDB()
                    link_id = insert_db._insert(tablename='wise_video_reply_shortvideo_0', **comment_dict)
                    print json.dumps(comment_dict, indent=2)
                    pass
                except Exception as ee:
                    print ee
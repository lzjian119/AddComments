#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-12-07 12:01:53
# Project: kuaishou_api

from pyspider.libs.base_handler import *
from pyspider.libs import mimod
from pyspider.libs.check import CheckData
from pyspider.libs.create_sign import creat_sign_f64
from pyspider.libs.daku_spider.common_redis_queue import CommonSet
from pyspider.libs import replydb
import hashlib
import hmac
import base64
import urllib
import datetime
import time, json
import re

check_data = CheckData()


class Handler(BaseHandler):
    crawl_config = {
        "proxy": "192.168.80.59:8889"
    }

    comment_url = 'https://live.kuaishou.com/graphql'

    comment_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36',
        'content-type': 'application/json',
        'Accept-Language': 'zh-CN'
    }

    common_set = CommonSet("kuaishou_comment")

    @every(minutes=60)
    def on_start(self):
        api_tpl = 'http://www.kuaishou.com/sitemap/baiduVideo/queryEntity?signature={0}&queryDate={1}&number={2}'
        number = 2000
        for i in range(7, 15):
            now = datetime.datetime.now()
            date = now.strftime('%Y%m%d')
            sign = self.calculate_sign(number, date)
            url = api_tpl.format(sign, date, number)
            print url
            self.crawl(url, callback=self.index_page)

    @staticmethod
    def calculate_sign(number, date):
        secret = bytes('ftGSrGcfJry7R73y').encode('utf-8')
        message = bytes('number={0}&queryDate={1}'.format(number, date)).encode('utf-8')
        signature = urllib.quote(base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest()))
        return signature

    @config(age=1)
    def index_page(self, response):
        # print response.text
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
                res['title'] = u'标题不存在_' + sign  # each['caption']
            res['author'] = each['userName']
            res['link'] = each['contentUrl'].split('?')[0]
            print res['link']
            # vid = re.findall('postRoll-(.*?).mp4', res['link'])[0]
            # res['link'] = 'http://jsmov2.a.yximgs.com/bs2/newWatermark/{0}_zh_4.mp4'.format(vid)
            # print res['link']
            res['block'] = u'现场'
            res['play_count'] = each['viewCount']
            res['comment_count'] = 0
            res['pub_time'] = int(time.time())
            res['site'] = 'kuaishouapi2'
            # print json.dumps(res,indent=2)
            result = check_data.check(res)
            if result['num'] == 0:
                try:
                    logger.info('send to mimod: %s', str(result['dict']))
                    ret, code, resp = mimod.send_to_mimod(result['dict'])
                    print json.dumps(result['dict'], indent=2)

                    # 获取网页版界面
                    live_url = each['sharingLink']
                    # live_url = 'https://live.kuaishou.com/u/{0}/{1}'.format(each['userId'], each['id'])
                    url = self.comment_url + '#' + each['id']
                    data = Handler.get_comment_request_data(each['id'])
                    print(data)
                    self.crawl(url,
                               headers=self.comment_headers,
                               callback=self.comment_page,
                               method='POST',
                               data=json.dumps(data),
                               save={'link': url, 'block': res['block'], 'photoId': each['id'], 'page': 1})
                except Exception as ee:
                    print ee
            else:
                print result['error']

    @config(priority=2)
    def comment_page(self, response):
        response.encoding = 'utf8'
        link = response.save['link']
        block = response.save['block']
        photo_id = response.save['photoId']
        j = response.json
        get_comment_list = j['data']['getCommentList']
        pcursor = get_comment_list['pcursor']
        page = response.save['page']

        for each in get_comment_list['commentList']:
            comment_dict = {}
            link_sign1, link_sign2 = creat_sign_f64(link)
            comment_dict['link_sign1'] = link_sign1
            comment_dict['link_sign2'] = link_sign2
            comment_dict['worksname'] = block
            comment_dict['uname'] = each['authorName'].replace('\n', '').strip()
            comment_dict['uicon'] = each['headurl'].replace('\n', '').strip()
            comment_dict['pubtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            comment_dict['cs'] = 'kuaishouapi2'
            comment_dict['info'] = each['content'].replace('\n', '').strip()

            print('len=%d,%s' % (len(comment_dict['info']), comment_dict['info']))
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
                except Exception as ee:
                    print ee

        if pcursor != "no_more" and 200 > (page * 20):
            url = self.comment_url + '#' + photo_id
            data = Handler.get_comment_request_data(photo_id, pcursor=pcursor)
            self.crawl(url,
                       headers=self.comment_headers,
                       callback=self.comment_page,
                       method='POST',
                       data=json.dumps(data),
                       save={'link': link, 'block': block, 'photoId': photo_id, 'pcursor': pcursor, 'page': page + 1})


    # 获取评论请求接口中的data
    @staticmethod
    def get_comment_request_data(photo_id, **kwargs):

        if not isinstance(photo_id, six.string_types):
            print('photoId参数类型错误')
            return {}

        pcursor = ""
        if kwargs.get('pcursor') and isinstance(kwargs.get('pcursor'), six.string_types):
            pcursor = kwargs['pcursor']

        data = {"operationName": "CommentFeeds",
                "variables": {"photoId": photo_id, "page": 1, "pcursor": pcursor, "count": 20},
                "query": "query CommentFeeds($photoId: String, $page: Int, $pcursor: String, $count: Int) {\n  getCommentList(photoId: $photoId, page: $page, pcursor: $pcursor, count: $count) {\n    commentCount\n    realCommentCount\n    pcursor\n    commentList {\n      ...BaseComment\n      subCommentCount\n      subCommentsPcursor\n      likedCount\n      liked\n      subComments {\n        commentId\n        replyToUserName\n        timestamp\n        content\n        authorName\n        authorId\n        replyTo\n        authorEid\n        headurl\n        replyToEid\n        status\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment BaseComment on BaseComment {\n  commentId\n  authorId\n  authorName\n  content\n  headurl\n  timestamp\n  authorEid\n  status\n  __typename\n}\n"}

        return data
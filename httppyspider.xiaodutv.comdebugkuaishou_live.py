#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-08-22 18:19:52
# Project: kuaishou_live

from pyspider.libs.base_handler import *
import json
import time
from pyspider.libs.check import CheckData
from pyspider.libs import mimod
check_data = CheckData()
from pyspider.libs import replydb
from pyspider.libs.create_sign import creat_sign_f64
from pyspider.libs.daku_spider.common_redis_queue import CommonSet
from pyspider.libs.daku_spider.redis_queue import CrawlSet
import hashlib
import re

def md5_str(str):
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()

class Handler(BaseHandler):
    crawl_config = {
        'itag':time.time()
    }
    
    urls = {
        'https://live.kuaishou.com/profile/AK666666':[u'搞笑达人','爆笑热门搞笑'],
        'https://live.kuaishou.com/profile/3xf56hhuenmwp89':[u'搞笑达人','二人转小火苗'],
        #'https://live.kuaishou.com/profile/3xjnhn3g7ztivua':[u'搞笑达人','一只刘小屁'],
        #'https://live.kuaishou.com/profile/Wendy-521':[u'搞笑达人','唤唤条子哥最美女弟子'],
        #'https://live.kuaishou.com/profile/3xx9fftvt3k7g54':[u'搞笑达人','搞笑军歌儿'],
        #'https://live.kuaishou.com/profile/DB3344521':[u'搞笑达人','铛铛'],
        #'https://live.kuaishou.com/profile/YZ66666666':[u'搞笑达人','Y泽'],
        #'https://live.kuaishou.com/profile/sm112233':[u'搞笑达人','三哥pk三嫂'],
        #'https://live.kuaishou.com/profile/KSLT6666':[u'搞笑达人','姚大'],
        #'https://live.kuaishou.com/profile/Aa361292971':[u'搞笑达人','孙英俊'],
        #'https://live.kuaishou.com/profile/3xx2bbqpk5dce7m':[u'搞笑达人','哈尔滨晶迪'],
        'https://live.kuaishou.com/profile/3xd23e7rpv9i5yg':[u'搞笑达人','搞笑大神'],
        'https://live.kuaishou.com/profile/3xpvq6e6pw35c6y':[u'搞笑达人','冷月大人'],
        'https://live.kuaishou.com/profile/xiuzhenxiaoali':[u'搞笑达人','袖珍小啊立'],
        'https://live.kuaishou.com/profile/3xju5d42cfu7qn6':[u'搞笑达人','啊衣诺'],
        'https://live.kuaishou.com/profile/wg17888888':[u'搞笑达人','魏博士'],
        'https://live.kuaishou.com/profile/BSP33333':[u'搞笑达人','茂名冰三炮'],
        'https://live.kuaishou.com/profile/su88888888':[u'搞笑达人','演员苏'],
        'https://live.kuaishou.com/profile/XWQ490959116':[u'明星达人','老夏在帝都（明星发布会）'],
        'https://live.kuaishou.com/profile/HY666666':[u'明星达人','演员～宏义（直播明星拍戏'],
        'https://live.kuaishou.com/profile/3xz9s76wjf7a9zu':[u'明星达人','虹桥绿毛哥拍明星不追星'],
        'https://live.kuaishou.com/profile/Yulezhuzhan':[u'明星达人','北京娱乐驻站'],
        'https://live.kuaishou.com/profile/3xvd7ppqja3sfmy':[u'生活达人','小妙招生活小窍门（清清）',u'修改标题'],
        'https://live.kuaishou.com/profile/Longjiao520':[u'生活达人','辰辰生活小窍门',u'修改标题'],
        'https://live.kuaishou.com/profile/3xejienzng72yyk':[u'生活达人','生活技巧叶',u'修改标题'],
        'https://live.kuaishou.com/profile/3xnkq6nip59x7zu':[u'明星达人','猫眼大明星'],
        'https://live.kuaishou.com/profile/3x85w58cpadnafq':[u'明星达人','虹桥一哥拍明星'],
    }
    
    data = '{"principalId": "%s", "pcursor": "%s", "count": 24, "privacy": "public"}'
    
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json',
    }
    
    common_set = CommonSet("kuaishou_comment")
    video_set = CrawlSet('kuaishou_video')

    @every(minutes=60)
    def on_start(self):
        for k,v in self.urls.items():
            url = k
            self.crawl(url, callback=self.index_page, save=v)

    @config(age=1)
    def index_page(self, response):
        block = response.save[0]
        author = response.save[1]
        if len(response.save)==3:
            print(response.save[2])
            title_flag=1
        else:
            title_flag=0
        j = json.loads(response.text.split('"tabDatas":{"open":')[1].split(',"private":')[0])
        #print json.dumps(j,indent=2)
        eid = ""
        for each in j['list']:
            res = {}
            
            try:
                res['link'] = each["playUrl"].replace('https','http')
            
                #print(res['link'])
                #video_id = re.findall(r'http://.*/(.*?)\.mp4', res['link'])
                #print(video_id)
                video_id = re.search(r'http://.*/(.*?)\.mp4', res['link']).group(1)
            except (KeyError,AttributeError):
                continue
            
            if self.video_set.ismember(video_id):
                continue
            else:
                self.video_set.add(video_id)
            res['title'] = each['caption']
            if title_flag:
                res['title']="标题不存在_{}".format(md5_str(res['link']))
            res['duration'] = 0
            res['vertical_thumnail_url'] = ''
            res['horizontal_thumnail_url'] = each['thumbnailUrl'].replace('https','http')
            res['description'] = ''
            res['author'] = author
            res['block'] = block
            res['site'] = 'kuaishou'
            res['play_count'] = "0"
            cmcnt = each['commentCount']
            if 'w' in each['commentCount']:
                cmcnt = each['commentCount'].replace('w','')
                cmcnt = int(float(cmcnt*10000))
            res['comment_count'] = cmcnt
            res['pub_time'] = int(each['timestamp']/1000)
            #eid = each['eid']替换
            eid=each['user']['id']
            result = check_data.check(res)
            if result['num']==0:
                try:
                    logger.info('send to mimod: %s', str(result['dict']))
                    ret, code, resp = mimod.send_to_mimod(result['dict'])
                    print ret, code, resp
                    print json.dumps(result['dict'],indent=2)
                    url = "https://live.kuaishou.com/u/%s/%s" % (each['user']['id'],each['photoId'])
                    self.crawl(url, save=[url,block], callback=self.comment_page)
                except Exception as ee:
                    print ee
                    continue
            else:
                print result['error']
            
            if j['pcursor'] != "no_more":
                data = self.data % (eid,j['pcursor'])
                self.crawl('https://live.kuaishou.com/feed/profile',callback=self.detail_page,save=[block,author,title_flag],headers=self.headers,method="POST",data=data)
            

    @config(priority=2)
    def detail_page(self, response):
        block,author,title_flag = response.save
        j = response.json
        #print json.dumps(j,indent=2)
        eid = ""
        for each in j['list']:
            res = {}

            res['link'] = each['playUrl'].replace('https','http')
            res['title'] = each['caption']
            if title_flag:
                res['title']="标题不存在_{}".format(md5_str(res['link']))
            res['duration'] = 0
            res['vertical_thumnail_url'] = ''
            res['horizontal_thumnail_url'] = each['thumbnailUrl'].replace('https','http')
            res['description'] = ''
            res['author'] = author
            res['block'] = block
            res['site'] = 'kuaishou'
            res['play_count'] = "0"
            cmcnt = each['commentCount']
            if 'w' in each['commentCount']:
                
                cmcnt = each['commentCount'].replace('w','')
                
                cmcnt = int(float(cmcnt)*10000)
            res['comment_count'] = cmcnt
            res['pub_time'] = int(each['timestamp']/1000)
            eid = each['user']['id']#each['eid']
            result = check_data.check(res)
            if result['num']==0:
                try:
                    logger.info('send to mimod: %s', str(result['dict']))
                    ret, code, resp = mimod.send_to_mimod(result['dict'])
                    print ret, code, resp
                    print json.dumps(result['dict'],indent=2)
                    url = "https://live.kuaishou.com/u/%s/%s" % (each['user']['id'],each['photoId'])
                    self.crawl(url, save=[res['link'],block], callback=self.comment_page)
                except Exception as ee:
                    print ee
                    continue
            else:
                print result['error']
            
            if j['pcursor'] != "no_more":
                data = self.data % (eid,j['pcursor'])
                self.crawl('https://live.kuaishou.com/feed/profile',callback=self.detail_page,save=[block,author,title_flag],headers=self.headers,method="POST",data=data)
    
    
    @config(priority=2)
    def comment_page(self, response):
        link,block = response.save
        et = response.etree
        for each in et.xpath('//div[@class="comment"]/div[@class="comment-item"]'):
            comment_dict = {}
            link_sign1,link_sign2=creat_sign_f64(link)
            comment_dict['link_sign1'] = link_sign1
            comment_dict['link_sign2'] = link_sign2
            comment_dict['worksname'] = block
            comment_dict['uname'] = each.xpath('.//div[@class="comment-item-author"]/a/text()')[0].replace('\n','').strip()
            comment_dict['uicon'] = each.xpath('.//div[@class="comment-item-author"]/a/text()')[0].replace('\n','').strip()
            comment_dict['pubtime'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            comment_dict['cs'] = 'kuaishou'
            comment_dict['info'] = each.xpath('.//span[@class="comment-item-content"]/span/text()')[0].replace('\n','').strip()
            md5_string = link + comment_dict['uname'] + comment_dict['info']
            cid = hashlib.md5(md5_string.encode('utf-8')).hexdigest()
            
            if self.common_set.ismember(cid):
                pass
            else:
                self.common_set.add(cid)
                try:
                    insert_db = replydb.REPLYDB()
                    link_id = insert_db._insert(tablename='wise_video_reply_shortvideo_0',**comment_dict)
                    print json.dumps(comment_dict,indent=2)  
                except Exception as ee:
                    print ee

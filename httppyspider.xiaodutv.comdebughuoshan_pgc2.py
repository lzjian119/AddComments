#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-10-29 19:14:30
# Project: huoshan_pgc2

from pyspider.libs import replydb
from pyspider.libs.create_sign import creat_sign_f64
from pyspider.libs.base_handler import *
from pyspider.libs import mimod
from pyspider.libs.check import CheckData
from pyspider.libs.dc.dc import dead_detect
from pyspider.libs.daku_spider.common_redis_queue import CommonSet
from pyspider.libs import common
from pyspider.libs import utils
import urllib
import urllib2
import random
import hashlib

check_data = CheckData()
import time, json, re


def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m

    return None


def get_rand_time():
    hours_dis = 72
    return int(time.time()) - random.randint(1, hours_dis * 3600)


def md5_str(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'com.ss.android.ugc.live/490 (Linux; U; Android 8.1.0; zh_CN; MI 8 SE; Build/OPM1.171019.019; Cronet/58.0.2991.0)'}
    }

    common_set = CommonSet("huoshan")
    block7 = u'生活达人'
    block8 = u'唱歌达人'
    block9 = u'明星达人'
    block10 = u'美食达人'
    site = "huoshan"

    @every(minutes=2 * 60)
    def on_start(self):
        '''from pyspider.libs.del_key import del_key
        try:
            del_key('%s' % self.project_name)
        except Exception as ee:
            print ee'''

        crawl_url_arr = [
            [
                'https://api.huoshan.com/hotsoon/user/95436620600/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540798311676&ts=1540798309&as=a2a55b1d35a6fbe7564355&cp=b167be5d5a6bda75e2QeYi&mas=00f18478cfc43cd3c2dae93f721f067c1e8e6aaee206686eb3',
                self.block7,
                '辣妈艾小鑫'],
            [
                'https://api.huoshan.com/hotsoon/user/89852523288/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799195564&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799195&as=a2e57bbdfb0debba664355&cp=b5d9bf51b668d7a4e2KoSw&mas=007b54f4f1cbdf67237818b77d6ce49b9eea0ca2e206686e95',
                self.block7,
                '小蝌蚪妈妈-'],
            [
                'https://api.huoshan.com/hotsoon/user/72319437328/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799502727&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799500&as=a2253b2d1c401b4cf64355&cp=be0cb65dc566dccde2So[w&mas=00ba69acea62a977e1dc74f16d2ed3d6eb0c0202e206686ef2',
                self.block7,
                '生活小妙招❤'],
            [
                'https://api.huoshan.com/hotsoon/user/62500774375/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799335677&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799333&as=a215ebdd9596bbab464355&cp=bf66be525966deb7e2Yoaw&mas=009e65c6940b0a8a3f02bc60856ccb15a72640a6e206686ea6',
                self.block7,
                '生活小窍门（段阿姨）'],

            [
                'https://api.huoshan.com/hotsoon/user/72319437328/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799502727&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799500&as=a2253b2d1c401b4cf64355&cp=be0cb65dc566dccde2So[w&mas=00ba69acea62a977e1dc74f16d2ed3d6eb0c0202e206686ef2',
                self.block7,
                '生活小妙招❤'],
            [
                'https://api.huoshan.com/hotsoon/user/71958438171/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799696678&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799696&as=a2f5bb1d404d3b2c364355&cp=badcb6500d64d0cee2_oMw&mas=006a46f7ea0a4f09e703aebd490d8936b10aa8a8e206686e92',
                self.block7,
                '点子生活小妙招��'],
            [
                'https://api.huoshan.com/hotsoon/user/76095202472/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799823773&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799823&as=a2152bbdaf34bb7d464355&cp=b94ebd51f66ad3d9e2_oMw&mas=006df7ed7aa98569a3baef601124bd9881e046a6e206686ec5',
                self.block7,
                '生活小窍门☀娟'],
            [
                'https://api.huoshan.com/hotsoon/user/61656960238/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799923897&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799923&as=a2352b9d034b9b6d464355&cp=b3bab657366dd2dee2Uo]w&mas=003fbabcf9cbcdfe30b6d18cbf5a411af1e846a6e206686ed5',
                self.block10,
                '达人美食哥'],
            [
                'https://api.huoshan.com/hotsoon/user/61647948840/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540800026724&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540800026&as=a2653b5daab12bfed64355&cp=b915b25cad65dae1e2[oIs&mas=00d66c61cf4133d356257ed5d04b51e621c84406e206686ed1',
                self.block7,
                '大雁美食分享'],
            [
                'https://api.huoshan.com/hotsoon/user/69906816893/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540800146403&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540800146&as=a2c59b3d52896baef64355&cp=b793b7532a63dde0e2MoUs&mas=00423952bf688802e1e4d1a0967320d84cc60402e206686ea1',
                self.block10,
                '美食��锅边舞��'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/73496691252/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=500&iid=48618496980&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=500&version_name=5.0.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=500&resolution=1080*2114&dpi=440&update_version_code=5008&_rticket=1541151899120&mcc_mnc=46001&ts=1541151899&as=a2a5e1edab391b8c5c6833&cp=129db45ab2ccd9c9e2Sc[g&mas=00cda68f730e09a34715b17aa18249fdf80fc80408d2050834',
                self.block9,
                '娱乐圈小㊙'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/61147500460/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=500&iid=48618496980&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=500&version_name=5.0.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=500&resolution=1080*2114&dpi=440&update_version_code=5008&_rticket=1541152324407&mcc_mnc=46001&ts=1541152324&as=a225e1bda4049b2e7c6855&cp=1049b35643c0d2efe2McUg&mas=00b2cf972f04cc39f2de5484ab348dcd646a8e0008d2656e94',
                self.block7,
                '羽瞳趣味妙招百科'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/78650353921/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=500&iid=48618496980&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=500&version_name=5.0.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=500&resolution=1080*2114&dpi=440&update_version_code=5008&_rticket=1541152501351&mcc_mnc=46001&ts=1541152501&as=a24531ad95cf7bceac8777&cp=1dffb05a56c4d5e7e2OiWq&mas=00e495481988821dff542a57322f8ebe81c2e4a678252a2a85',
                self.block7,
                '静静爱分享'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/70961809510/items/?max_time=1541592534000&offset=20&count=20&req_from=feed_loadmore&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542177957404&ts=1542177955&as=a2750c1e03ba9bc41b4411&cp=cea2b1593dbce745e2IuQy&mas=00a74b28e0b62e11bd841de6cbd3ba61be48468640e6464cd2',
                self.block10,
                '爱生活爱美食'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/71515824773/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542178455384&ts=1542178453&as=a2e56c2e15996b063b4644&cp=ce90b75c5bbae367e2_uMy&mas=00a550e4aebda71edcbeefc5bc796087a4a4028240a6e2e6ef',
                self.block10,
                '橙子小厨'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/71314306516/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542178583014&ts=1542178581&as=a2e58c2e45b19bd7eb4466&cp=cd18bb5a56bce27be2Uu]y&mas=008bd4deb6f45c4283277cca5b4ba4743b86602440e6a6a2af',
                self.block10,
                '雁姐美食厨房'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/61478885027/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
                self.block10,
                '刘小六(六六妖儿)'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/75071680688/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
                self.block9,
                '走着走着就遇到了明星'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/70420237537/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
                self.block9,
                '娱乐众生相'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/68373658506/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
                self.block9,
                '徐泾十三点King'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/52749989616/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
                self.block9,
                '娱乐大汇总'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/16904494572/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
                self.block9,
                '雾霾天看月亮'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/104559470960/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
                self.block9,
                '明星跟拍小黄鸭'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/85971783620/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
                self.block9,
                '明星跟拍(经纪人)'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/81176424347/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
                self.block9,
                '明星街拍Show'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/82840103833/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
                self.block9,
                '段桥雪'],
            [
                'https://hotsoon.snssdk.com/hotsoon/user/75116226491/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
                self.block9,
                '娱乐oncall'],

        ]

        for i in range(0, len(crawl_url_arr)):
            info_obj = crawl_url_arr[i]
            if len(info_obj) < 3:
                continue

            crawl_url = info_obj[0]

            block = info_obj[1]

            print info_obj[2]
            # print info_obj

            self.crawl(
                crawl_url,
                method="GET",
                callback=self.index_page,
                itag=time.time(),
                save=block)

        crawl_huati_arr = [
            [
                'https://hotsoon.snssdk.com/hotsoon/hashtag/1594330990140446/items/?min_time=0&offset={}&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540867552873&ab_version=391711%2C564003%2C570935%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C568545%2C570099%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C571139%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C457535%2C523976%2C571445%2C550979&ts=1540867552&as=a2859c9d302e9b35f74355&cp=c5eab557037cd65ce2IyQc&mas=0068eab4083ef4822e6039332eeda2d2ee68a482ea06686ed4',
                self.block7,
                '生活话题'],
            [
                'https://api.huoshan.com/hotsoon/hashtag/1593526267487236/items/?min_time=0&offset={}&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540868350937&ab_version=391711%2C564003%2C570935%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C568545%2C570099%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C571139%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C457535%2C523976%2C571445%2C550979&ts=1540868350&as=a2b58c7d6e7f6b68774355&cp=c5fdb65fe87dd584e2[cIg&mas=001ed94a035723313a404786bb262ab8f0d2252aea06686e89',
                self.block7,
                '美食话题'],
            [
                'https://hotsoon.snssdk.com/hotsoon/hashtag/1593526267443220/items/?min_time=0&offset={}&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540870538296&ab_version=391711%2C564003%2C570935%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C568545%2C570099%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C571139%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C457535%2C523976%2C571445%2C550979&ts=1540870538&as=a285ed3d6a687be1074355&cp=dc82b559ab70df1be2[yIc&mas=002ddf3add07d294e13671690325356312eecc24ea06686eb5',
                self.block8,
                '唱歌话题']
        ]
        for i in range(0, len(crawl_huati_arr)):
            info_obj = crawl_huati_arr[i]
            url = info_obj[0]
            block = info_obj[1]
            print info_obj[2]
            # print info_obj
            for num in range(251):
                crawl_url = url.format(num * 20)
                print(crawl_url)
                self.crawl(
                    crawl_url,
                    method="GET",
                    callback=self.index_page,
                    itag=time.time(),
                    save=block)

    @config(age=1 * 1 * 1 * 60)
    def index_page(self, response):
        json_obj = response.json
        block = response.save

        try:
            data_list = json_obj["data"]
        except TypeError as e:
            print('error', e)
            return
        site = self.site
        insert_arr = []
        for each in data_list:
            data_info = each["data"]
            video = data_info["video"]

            res = {}
            play_url = video["url_list"][0]
            '''
            if compare_mo_url_hour(play_url) == False:
                print "pass:",play_url
                continue
            '''

            res['link'] = re.sub('&ts=\d{10}', '', play_url)
            res['title'] = data_info["title"]
            if len(res['title']) < 1:
                res['title'] = "标题不存在_{}".format(md5_str(play_url))

            res['duration'] = video["duration"]
            res['vertical_thumnail_url'] = ''
            res['horizontal_thumnail_url'] = video["cover"]["url_list"][0].replace('.webp', '')
            res['description'] = ''
            res['author'] = data_info["author"]["id"]

            res['block'] = block
            res['site'] = site
            res['play_count'] = "0"
            res['comment_count'] = data_info['stats']['comment_count']
            res['pub_time'] = data_info["create_time"]

            # return res
            result = check_data.check(res)
            # print json.dumps(result['dict'],indent=4)
            # return result
            # vid = re.sub("\?.+","",play_url)

            if result['num'] == 0:
                try:
                    logger.info('send to mimod: %s', str(result['dict']))
                    if utils.check_image(res['horizontal_thumnail_url']) == 1:
                        print 111111
                        ret, code, resp = mimod.send_to_mimod(result['dict'])
                        print "=========== SEND ==========="
                        print json.dumps(result['dict'], indent=4)

                        # 抓取评论
                        comment_count = min(res['comment_count'], 200)
                        for i in range(0, comment_count, 20):
                            url = "https://hotsoon.snssdk.com/hotsoon/item/%s/comments/?offset=%d&count=20&live_sdk_version=280&iid=17973913310&device_id=29535583655&ac=wifi&channel=tengxun&aid=1112&app_name=live_stream&version_code=280&version_name=2.8.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&os_api=23&os_version=6.0.1&uuid=359320050951630&openudid=c4d0375ebc82b961&manifest_version_code=280&resolution=1440*2392&dpi=560&update_version_code=2802&ts=%d&as=a235e5018df48a2fc2&cp=574fa65adc271cf0e2" % (
                                each['data']['id_str'], i, int(time.time()))
                            print"999999:", url
                            self.crawl(url, callback=self.detail_page, save={'link': res['link'], 'block': block})

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

            icon = comment['user']['avatar_jpg']['url_list'][0]
            comment_dict['uicon'] = icon
            comment_dict['pubtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            # print comment_dict['pubtime']
            comment_dict['cs'] = 'huoshan'
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












#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-10-29 19:14:30
# Project: huoshan_pgc2

from pyspider.libs import replydb
from pyspider.libs.create_sign import creat_sign_f64
from pyspider.libs.base_handler import *
from pyspider.libs import mimod
from pyspider.libs.check import CheckData
from pyspider.libs.dc.dc import dead_detect
from pyspider.libs.daku_spider.common_redis_queue import CommonSet
from pyspider.libs import common
from pyspider.libs import utils
import urllib
import urllib2
import random
import hashlib
check_data = CheckData()
import time,json,re

def r1(pattern, text): 
    m = re.search(pattern, text)
    if m:
        return m
    
    return None

def get_rand_time():
    hours_dis = 72
    return int(time.time()) - random.randint(1,hours_dis*3600)

def md5_str(str):
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()



class Handler(BaseHandler):
    crawl_config = {
        'headers':{'User-Agent': 'com.ss.android.ugc.live/490 (Linux; U; Android 8.1.0; zh_CN; MI 8 SE; Build/OPM1.171019.019; Cronet/58.0.2991.0)'}
    }
    
    common_set = CommonSet("huoshan")
    block7=u'生活达人'
    block8=u'唱歌达人'
    block9=u'明星达人'
    block10=u'美食达人'
    site = "huoshan"

    @every(minutes=2 * 60)
    def on_start(self):
        '''from pyspider.libs.del_key import del_key
        try:
            del_key('%s' % self.project_name)
        except Exception as ee:
            print ee'''
            
        crawl_url_arr = [
            ['https://api.huoshan.com/hotsoon/user/95436620600/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540798311676&ts=1540798309&as=a2a55b1d35a6fbe7564355&cp=b167be5d5a6bda75e2QeYi&mas=00f18478cfc43cd3c2dae93f721f067c1e8e6aaee206686eb3',
             self.block7,
             '辣妈艾小鑫'],
            ['https://api.huoshan.com/hotsoon/user/89852523288/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799195564&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799195&as=a2e57bbdfb0debba664355&cp=b5d9bf51b668d7a4e2KoSw&mas=007b54f4f1cbdf67237818b77d6ce49b9eea0ca2e206686e95',
            self.block7,
            '小蝌蚪妈妈-'],
            ['https://api.huoshan.com/hotsoon/user/72319437328/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799502727&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799500&as=a2253b2d1c401b4cf64355&cp=be0cb65dc566dccde2So[w&mas=00ba69acea62a977e1dc74f16d2ed3d6eb0c0202e206686ef2',
            self.block7,
            '生活小妙招❤'],
            ['https://api.huoshan.com/hotsoon/user/62500774375/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799335677&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799333&as=a215ebdd9596bbab464355&cp=bf66be525966deb7e2Yoaw&mas=009e65c6940b0a8a3f02bc60856ccb15a72640a6e206686ea6',
            self.block7,
            '生活小窍门（段阿姨）'],
            
            ['https://api.huoshan.com/hotsoon/user/72319437328/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799502727&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799500&as=a2253b2d1c401b4cf64355&cp=be0cb65dc566dccde2So[w&mas=00ba69acea62a977e1dc74f16d2ed3d6eb0c0202e206686ef2',
            self.block7,
            '生活小妙招❤'],
            ['https://api.huoshan.com/hotsoon/user/71958438171/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799696678&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799696&as=a2f5bb1d404d3b2c364355&cp=badcb6500d64d0cee2_oMw&mas=006a46f7ea0a4f09e703aebd490d8936b10aa8a8e206686e92',
            self.block7,
            '点子生活小妙招��'],
            ['https://api.huoshan.com/hotsoon/user/76095202472/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799823773&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799823&as=a2152bbdaf34bb7d464355&cp=b94ebd51f66ad3d9e2_oMw&mas=006df7ed7aa98569a3baef601124bd9881e046a6e206686ec5',
            self.block7,
            '生活小窍门☀娟'],
            ['https://api.huoshan.com/hotsoon/user/61656960238/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540799923897&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540799923&as=a2352b9d034b9b6d464355&cp=b3bab657366dd2dee2Uo]w&mas=003fbabcf9cbcdfe30b6d18cbf5a411af1e846a6e206686ed5',
            self.block10,
            '达人美食哥'],
            ['https://api.huoshan.com/hotsoon/user/61647948840/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540800026724&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540800026&as=a2653b5daab12bfed64355&cp=b915b25cad65dae1e2[oIs&mas=00d66c61cf4133d356257ed5d04b51e621c84406e206686ed1',
            self.block7,
            '大雁美食分享'],
            ['https://api.huoshan.com/hotsoon/user/69906816893/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540800146403&ab_version=391711%2C564003%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C560566%2C568545%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C569964%2C457535%2C523976%2C550979&ts=1540800146&as=a2c59b3d52896baef64355&cp=b793b7532a63dde0e2MoUs&mas=00423952bf688802e1e4d1a0967320d84cc60402e206686ea1',
            self.block10,
            '美食��锅边舞��'],
            ['https://hotsoon.snssdk.com/hotsoon/user/73496691252/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=500&iid=48618496980&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=500&version_name=5.0.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=500&resolution=1080*2114&dpi=440&update_version_code=5008&_rticket=1541151899120&mcc_mnc=46001&ts=1541151899&as=a2a5e1edab391b8c5c6833&cp=129db45ab2ccd9c9e2Sc[g&mas=00cda68f730e09a34715b17aa18249fdf80fc80408d2050834',
             self.block9,
             '娱乐圈小㊙'],
            ['https://hotsoon.snssdk.com/hotsoon/user/61147500460/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=500&iid=48618496980&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=500&version_name=5.0.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=500&resolution=1080*2114&dpi=440&update_version_code=5008&_rticket=1541152324407&mcc_mnc=46001&ts=1541152324&as=a225e1bda4049b2e7c6855&cp=1049b35643c0d2efe2McUg&mas=00b2cf972f04cc39f2de5484ab348dcd646a8e0008d2656e94',
            self.block7,
            '羽瞳趣味妙招百科'],
            ['https://hotsoon.snssdk.com/hotsoon/user/78650353921/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=500&iid=48618496980&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=500&version_name=5.0.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=500&resolution=1080*2114&dpi=440&update_version_code=5008&_rticket=1541152501351&mcc_mnc=46001&ts=1541152501&as=a24531ad95cf7bceac8777&cp=1dffb05a56c4d5e7e2OiWq&mas=00e495481988821dff542a57322f8ebe81c2e4a678252a2a85',
            self.block7,
            '静静爱分享'],
            ['https://hotsoon.snssdk.com/hotsoon/user/70961809510/items/?max_time=1541592534000&offset=20&count=20&req_from=feed_loadmore&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542177957404&ts=1542177955&as=a2750c1e03ba9bc41b4411&cp=cea2b1593dbce745e2IuQy&mas=00a74b28e0b62e11bd841de6cbd3ba61be48468640e6464cd2',
            self.block10,
            '爱生活爱美食'],
            ['https://hotsoon.snssdk.com/hotsoon/user/71515824773/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542178455384&ts=1542178453&as=a2e56c2e15996b063b4644&cp=ce90b75c5bbae367e2_uMy&mas=00a550e4aebda71edcbeefc5bc796087a4a4028240a6e2e6ef',
            self.block10,
            '橙子小厨'],
            ['https://hotsoon.snssdk.com/hotsoon/user/71314306516/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542178583014&ts=1542178581&as=a2e58c2e45b19bd7eb4466&cp=cd18bb5a56bce27be2Uu]y&mas=008bd4deb6f45c4283277cca5b4ba4743b86602440e6a6a2af',
            self.block10,
            '雁姐美食厨房'],
            ['https://hotsoon.snssdk.com/hotsoon/user/61478885027/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
            self.block10,
            '刘小六(六六妖儿)'],
            ['https://hotsoon.snssdk.com/hotsoon/user/75071680688/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
            self.block9,
            '走着走着就遇到了明星'],
            ['https://hotsoon.snssdk.com/hotsoon/user/70420237537/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
            self.block9,
            '娱乐众生相'],
             ['https://hotsoon.snssdk.com/hotsoon/user/68373658506/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
            self.block9,
            '徐泾十三点King'],
            ['https://hotsoon.snssdk.com/hotsoon/user/52749989616/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
            self.block9,
            '娱乐大汇总'],
            ['https://hotsoon.snssdk.com/hotsoon/user/16904494572/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
            self.block9,
            '雾霾天看月亮'],
            ['https://hotsoon.snssdk.com/hotsoon/user/104559470960/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
            self.block9,
            '明星跟拍小黄鸭'],
            ['https://hotsoon.snssdk.com/hotsoon/user/85971783620/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
            self.block9,
            '明星跟拍(经纪人)'],
            ['https://hotsoon.snssdk.com/hotsoon/user/81176424347/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
            self.block9,
            '明星街拍Show'],
            ['https://hotsoon.snssdk.com/hotsoon/user/82840103833/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
            self.block9,
            '段桥雪'],
            ['https://hotsoon.snssdk.com/hotsoon/user/75116226491/items/?min_time=0&offset=0&count=20&req_from=enter_auto&live_sdk_version=510&iid=51105766373&device_id=29535583655&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=510&version_name=5.1.0&device_platform=android&ssmix=a&device_type=Nexus+6&device_brand=google&language=zh&os_api=23&os_version=6.0.1&openudid=c4d0375ebc82b961&manifest_version_code=510&resolution=1440*2392&dpi=560&update_version_code=5103&_rticket=1542179040272&ts=1542179038&as=a2a55cfece0d5bf8cb4899&cp=c3d3b154e0bfe98ce2Wu_y&mas=0048a29ea077821a6dd0bfe1f760011382720f2240d6555d8f',
            self.block9,
            '娱乐oncall'],
            
            
        ]
        
     
        for i in range(0,len(crawl_url_arr)):
            info_obj = crawl_url_arr[i]
            if len(info_obj) < 3:
                continue
            
            crawl_url = info_obj[0]

            block = info_obj[1]
            
            print info_obj[2]
            #print info_obj
            
            self.crawl(
                crawl_url,
                method="GET",
                callback=self.index_page,
                itag=time.time(),
                save=block)
        
        
        crawl_huati_arr=[
            ['https://hotsoon.snssdk.com/hotsoon/hashtag/1594330990140446/items/?min_time=0&offset={}&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540867552873&ab_version=391711%2C564003%2C570935%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C568545%2C570099%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C571139%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C457535%2C523976%2C571445%2C550979&ts=1540867552&as=a2859c9d302e9b35f74355&cp=c5eab557037cd65ce2IyQc&mas=0068eab4083ef4822e6039332eeda2d2ee68a482ea06686ed4',
            self.block7,
            '生活话题'],
            ['https://api.huoshan.com/hotsoon/hashtag/1593526267487236/items/?min_time=0&offset={}&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540868350937&ab_version=391711%2C564003%2C570935%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C568545%2C570099%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C571139%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C457535%2C523976%2C571445%2C550979&ts=1540868350&as=a2b58c7d6e7f6b68774355&cp=c5fdb65fe87dd584e2[cIg&mas=001ed94a035723313a404786bb262ab8f0d2252aea06686e89',
            self.block7,
            '美食话题'],
            ['https://hotsoon.snssdk.com/hotsoon/hashtag/1593526267443220/items/?min_time=0&offset={}&count=20&req_from=enter_auto&live_sdk_version=490&iid=46543690249&device_id=57274498649&ac=wifi&channel=xiaomi&aid=1112&app_name=live_stream&version_code=490&version_name=4.9.0&device_platform=android&ssmix=a&device_type=MI+8+SE&device_brand=Xiaomi&language=zh&os_api=27&os_version=8.1.0&openudid=9335945ffc5d3945&manifest_version_code=490&resolution=1080*2114&dpi=440&update_version_code=4904&_rticket=1540870538296&ab_version=391711%2C564003%2C570935%2C564735%2C568853%2C565435%2C524274%2C564846%2C569581%2C570075%2C552683%2C493077%2C563413%2C557631%2C404280%2C568545%2C570099%2C552084%2C374105%2C563979%2C500305%2C488746%2C566020%2C465279%2C571139%2C482718%2C560494%2C567319%2C564958%2C299908%2C553786%2C457535%2C523976%2C571445%2C550979&ts=1540870538&as=a285ed3d6a687be1074355&cp=dc82b559ab70df1be2[yIc&mas=002ddf3add07d294e13671690325356312eecc24ea06686eb5',
            self.block8,
            '唱歌话题']
        ]
        for i in range(0,len(crawl_huati_arr)):
            info_obj = crawl_huati_arr[i]
            url = info_obj[0]
            block = info_obj[1]
            print info_obj[2]
            #print info_obj
            for num in range(251):
                crawl_url=url.format(num*20)
                print(crawl_url)
                self.crawl(
                    crawl_url,
                    method="GET",
                    callback=self.index_page,
                    itag=time.time(),
                    save=block)

    @config(age=1 * 1 * 1 * 60)
    def index_page(self, response):
        json_obj = response.json
        block = response.save
        
        try:
            data_list = json_obj["data"]
        except TypeError as e:
            print('error',e)
            return
        site = self.site
        insert_arr = []
        for each in data_list:
            data_info = each["data"]
            video = data_info["video"]

            res = {}
            play_url = video["url_list"][0]
            '''
            if compare_mo_url_hour(play_url) == False:
                print "pass:",play_url
                continue
            '''
            
            res['link'] =re.sub('&ts=\d{10}','',play_url)
            res['title'] = data_info["title"]
            if len(res['title']) < 1:
                res['title'] = "标题不存在_{}".format(md5_str(play_url))
                
                
            res['duration'] = video["duration"]
            res['vertical_thumnail_url'] = ''
            res['horizontal_thumnail_url'] = video["cover"]["url_list"][0].replace('.webp','')
            res['description'] = ''
            res['author'] = data_info["author"]["id"]
            
            res['block'] = block
            res['site'] = site
            res['play_count'] = "0"
            res['comment_count'] = 0
            res['pub_time'] = data_info["create_time"]
            
            #return res
            result = check_data.check(res)
            #print json.dumps(result['dict'],indent=4)
            #return result
            #vid = re.sub("\?.+","",play_url)
            
                

        
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
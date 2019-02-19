# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 20:01:05 2018

@author: ssun
"""

from urllib import request
import requests
from urllib import parse
import urllib
import random
import json
import toml

conf_file = "conf.toml"

ua_pool = [{'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
           {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
           {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
           {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
           {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/53"},
           {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
           ]

def get_comconf():
    '''
    获取配置当中的所有信息
    '''
    with open(conf_file, 'r') as conf_h:
        conf = toml.loads(conf_h.read())
    return conf["config"]
    

def get_ua():
    i = random.randint(0,len(ua_pool)-1)
    return ua_pool[i]


class Get_source(object):
    def __init__(self, music_name):
        self.music_name = music_name
    
    def get_data(self):
        '''
        通过歌曲名请求资源
        '''
        music_name_encode = parse.quote(self.music_name)
        url = '''http://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298
         &new_json=1&remoteplace=txt.yqq.center&t=0&aggr=1&cr=1&catZhida=1&lossless=0
         &flag_qc=0&p=1&n=100&w={}
         &&jsonpCallback=searchCallbacksong2020&format=jsonp&inCharset=utf8
         &outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'''.format(music_name_encode) 
        ua_header = get_ua()
        response = requests.get(url, headers = ua_header)
    
        if response.status_code == 200:
            data = response.text[9:-1]
        #print(data)
            detail = json.loads(data)
            return detail['data']
        return  None
    
    def search_detail(self):
        '''
        对获得的资源信息进行处理
        '''
        data = self.get_data()    
        music_all = data['song']['list']   
        music_list = []
        for i in music_all:
            dic = {}
            dic['song_name'] = i['name']    #歌曲名
            dic['singer_name'] = i['singer'][0]['name']   #歌手名
            dic['album_name'] = i['album']['name']#专辑名称
            dic['song_id'] = i['file']['media_mid']   #歌曲的id
            dic['format'] = i['file']
            dic['id'] = i['id']
            music_list.append(dic)
        return music_list

    def get_source(self, song_info):
        stream = get_comconf()['stream']
        guid = get_comconf()['guid']
        uin = get_comconf()['uin']
        fromtag = get_comconf()['fromtag']
    
        songmid = song_info['song_id']
        song_name = song_info['song_name']
        filename = 'C400' + songmid + '.m4a'
        url_getvkey = '''http://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=0&loginUin=1008611&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&uin=1008611&songmid=%s&filename=%s&guid=1234567890'''%(songmid, filename)
        #print(url_getvkey)
        response = requests.get(url_getvkey)
        #print(response.content)
        vkey = json.loads(response.content)['data']['items'][0]['vkey']
        #print(vkey)
        if len(vkey) < 100:
            return False
        name_ = 'F000' + str(songmid)
        # url_download = '''http://{0}/{1}.flac?vkey={2}&guid={3}&uin={4}&fromtag={5}'''.format(stream, name_, vkey, guid, uin, fromtag)
        # #print(url_download)
        # urllib.request.urlretrieve(url_download,'music/%s.flac'%song_name)
        # return True
        return stream, name_, vkey, guid, uin, fromtag,song_name

    def StartDownload(self, stream, name, vkey, guid, uin,fromtag,song_name):
        url_download = '''http://{0}/{1}.flac?vkey={2}&guid={3}&uin={4}&fromtag={5}'''.format(stream, name, vkey, guid, uin, fromtag)
        urllib.request.urlretrieve(url_download,'music/%s.flac'%song_name)   

if __name__ == '__main__':
    a = Get_source('猎户星座')
    a.get_source(a.search_detail()[0])





    




'''
http://streamoc.music.tc.qq.com/F000002aVLtc0ehh5p.flac?vkey=CEA84DCFB74C1130AF4F925E531A9BED3E1EBF814CE6F82C32A0694ABCAD5213FED4FB2A29FBA59E226E82413D3A66261FB28D21FBEB3521&guid=1234567890&uin=1008611&fromtag=8

http://streamoc.music.tc.qq.com/F000001DrzDT4FvTLO.flac?vkey=6C1F4A5BBE1DE0B2E999F8740991E42B94165E88741774D22F126D0D0EF05BAEE9CE2FAAE89359C7208A69A0E15DD9B59072A62456EF6A70&guid=1234567890&uin=1008611&fromtag=8


我最亲爱的：
http://streamoc.music.tc.qq.com/F000004Qgluz1XYdwp.flac?vkey=CEA84DCFB74C1130AF4F925E531A9BED3E1EBF814CE6F82C32A0694ABCAD5213FED4FB2A29FBA59E226E82413D3A66261FB28D21FBEB3521&guid=1234567890&uin=1008611&fromtag=8


http://streamoc.music.tc.qq.com/F0000049uvmV4509Le.flac?vkey=CEA84DCFB74C1130AF4F925E531A9BED3E1EBF814CE6F82C32A0694ABCAD5213FED4FB2A29FBA59E226E82413D3A66261FB28D21FBEB3521&guid=1234567890&uin=1008611&fromtag=8

http://streamoc.music.tc.qq.com/F000003HMC1n4GkNL8.flac?vkey=CEA84DCFB74C1130AF4F925E531A9BED3E1EBF814CE6F82C32A0694ABCAD5213FED4FB2A29FBA59E226E82413D3A66261FB28D21FBEB3521&guid=1234567890&uin=1008611&fromtag=8
'''

#get_source(search_detail()[0])

    
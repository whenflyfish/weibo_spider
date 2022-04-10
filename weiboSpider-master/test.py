# -*- coding: utf-8 -*-
#!/usr/bin/env python
import requests
import json
from urllib.parse import urlencode
import requests
import logging
from lxml import etree
def test():
    # url="https://weibo.com/ajax/profile/searchblog?uid=2058586920&page=1&feature=0&q=2022"
    # page = 1
    # params = {
    #     'uid':'2058586920',
    #     'page':page,
    #     'feature':'0',
    # }# 构造参数字典
    # headers = {
    #     'authority':'weibo.com',
    #     'Accept':'application/json, text/plain, */*',
    #     'path':'/ajax/profile/searchblog?uid=2058586920&page=1&feature=0&q=%E8%80%83%E7%A0%94',
    #     'Accept-Encoding':'gzip, deflate, br',
    #     'Accept-Language':'zh-CN,zh;q=0.8',
    #     'method':'GET',
    #     'Cookie':'login_sid_t=28a6a907d1bdc248ca72db1e2ab3a99f; cross_origin_proto=SSL; _ga=GA1.2.1485910075.1642229365; _s_tentry=-; Apache=260518605113.31125.1642229372518; SINAGLOBAL=260518605113.31125.1642229372518; ULV=1642229372528:1:1:1:260518605113.31125.1642229372518:; UOR=,,www.baidu.com; SSOLoginState=1644315414; XSRF-TOKEN=_3Edlr01bnKhe7trC8IcGV1x; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFWs-Ms.ZgeuxNSpQ4IyOiR5JpX5KMhUgL.FoM7eKMEeKeXe0q2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNeh2Neo20Shec; ALF=1681027044; SCF=AtdKXkSCgq_IsabmpRw5nTykzVp5aeRO1emih-W6uQ4fUdZ35Rv8wqE-PEmYXADYeARmxW_Blba7C90CgIcFLFc.; SUB=_2A25PVUw1DeRhGeFO6lUT8S3IyDqIHXVsIzr9rDV8PUNbmtAfLRf_kW9NQZBUBnPw4YOMNZd6nQJFbUtLew63cZ9V; WBPSESS=0sVsEZPhQFx8cksU1RWdZPbkCehMLTawOMovD_trToQ-PSfkziS5UH0cFdufdBMPRCzRSGwLNYV_wxmNV9AMw1bX4k9GNV-LQ-t93D5yzrTaaw3tPbZrKbg5mc0L2YbGdIXuYhqN_07SlFdwG0sGGQ==',
    #     'Referer':'https://weibo.com/u/2058586920',
    #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    #     'X-Requested-With':'XMLHttpRequest',
    #     'traceparent':'00-7a1bef92e896a02b53ef8f392cab2181-b6a62dadb7f5ca5b-00',
    #     'X-xsrf-token':'_3Edlr01bnKhe7trC8IcGV1x',
    #     'scheme':'https'
    #     }

    base_url = 'https://weibo.com/ajax/profile/searchblog?'
    headers = {
        'cookie': 'SCF=AtdKXkSCgq_IsabmpRw5nTykzVp5aeRO1emih-W6uQ4f0eIo3cNUAgOwPNbw31uhrx9MyA9lSegEixHZrMdnNiI.; SUB=_2A25PVhdtDeRhGeFO6lUT8S3IyDqIHXVsuLklrDV6PUJbktANLWv8kW1NQZBUBp59MrAJuq34VyJTXNnLxis8ZQf2; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFWs-Ms.ZgeuxNSpQ4IyOiR5NHD95QNeh2Neo20ShecWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS05pS0zpe0B0Sntt; SSOLoginState=1649567549',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    page = 1
    params = {
        'uid': '1499104401',
        'page': page,
        'feature': '0',
        'q':'乌',
    }  # 构造参数字典
    url = base_url + urlencode(params)  # 组合url
    try:
        resp = requests.get(url, headers=headers).text
        data = json.loads(resp)
        print(data)

    except requests.ConnectionError as e:
        print('Error', e.args)

test()
# print(selector.xpath("//*/text()"))
# try:
#     if selector.xpath("//input[@name='mp']") == []:
#         page_num = 1
#     else:
#         page_num = (int)(selector.xpath("//input[@name='mp']")
#                          [0].attrib['value'])
#     print(page_num)
# except Exception as e:
#     logger.exception(e)
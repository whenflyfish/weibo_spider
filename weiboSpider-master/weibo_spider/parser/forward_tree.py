import sys
from .util import handle_html
from parser import *
import re
import os
import queue
import time
import json
print(dir())
print(sys.path)

cookie = "SCF=AtdKXkSCgq_IsabmpRw5nTykzVp5aeRO1emih-W6uQ4f0eIo3cNUAgOwPNbw31uhrx9MyA9lSegEixHZrMdnNiI.; SUB=_2A25PVhdtDeRhGeFO6lUT8S3IyDqIHXVsuLklrDV6PUJbktANLWv8kW1NQZBUBp59MrAJuq34VyJTXNnLxis8ZQf2; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFWs-Ms.ZgeuxNSpQ4IyOiR5NHD95QNeh2Neo20ShecWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS05pS0zpe0B0Sntt; SSOLoginState=1649567549"
def find_forward(weiboid,uid,forward_tree,forward_queue):
    url = "https://weibo.cn/repost/"  + weiboid + "?uid=" + uid + "&page=1"
    #url = "https://weibo.cn/repost/LzWb4zFrf?uid=6617213711&rl=0&page=1"
    print(url)
    cookie = "SCF=AtdKXkSCgq_IsabmpRw5nTykzVp5aeRO1emih-W6uQ4f0eIo3cNUAgOwPNbw31uhrx9MyA9lSegEixHZrMdnNiI.; SUB=_2A25PVhdtDeRhGeFO6lUT8S3IyDqIHXVsuLklrDV6PUJbktANLWv8kW1NQZBUBp59MrAJuq34VyJTXNnLxis8ZQf2; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFWs-Ms.ZgeuxNSpQ4IyOiR5NHD95QNeh2Neo20ShecWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS05pS0zpe0B0Sntt; SSOLoginState=1649567549"
    selector = handle_html(cookie,url)
    # 存放所有的转发人的id
    uri_list = []
    try:
        # 查找有没有转发
        format_str = selector.xpath('//*[@id="rt"]/text()')
        format_num = re.findall(r"(?<=\[)\d+(?=\])", format_str[0])
        if len(format_num) == 0:
            forward_tree[weiboid] = uri_list
            print("无转发人")
            return
        # 查找转发页数
        page_num_str = selector.xpath('//*[@id="pagelist"]/form/div/text()')
        page_num_str = page_num_str[-1].split("/")[-1]
        page_num = re.findall(r"\d+",page_num_str)[-1]
        # print("page num :",page_num)
        total = 0
        # 遍历每一页，查找微博id和转发人的id
        for i in range(1,int(page_num)+1):
            url_page = "https://weibo.cn/repost/LzWb4zFrf?uid=6617213711&rl=0&page=" + str(i)
            print(url_page)
            selector = handle_html(cookie, url_page)
            weio_id = selector.xpath('//span[@class="cc"]/a/@href')
            uri = selector.xpath('//span[@class="cc"]/../a[1]/@href')
            # print(uri)
            # print(uri[0][1:])
            for j in range(len(weio_id)):
                # print(uri[i])
                uid = uri[j][1:]
                wid = weio_id[j].split("/")[2]
                forward_queue.put((wid,uid))
                uri_list.append(uid)
            total = total + len(weio_id)
            # print("weio_id: ",weio_id)
            # print("uri: ",uri)
            # print("weibo_id number : ",len(weio_id))
            # print("uri number : ", len(uri))
            time.sleep(1)
        # print("number_id: ",total)
        # print(weibo_id_list)
        # print(uri_list)
    except:
        print("未找到{}的转发树".format(url))
    forward_tree[weiboid] = uri_list

def get_uid(weiboid):
    url = "https://weibo.cn/repost/"  + weiboid
    selector = handle_html(cookie,url)
    try:
        uid = selector.xpath('//*[@id="M_"]/div[1]/a[1]/@href')[0][1:]
    except:
        print("未找到id")
        return ""
    return uid

def find_forward_new(weiboid):
    url = "https://weibo.cn/repost/"  + weiboid
    #url = "https://weibo.cn/repost/LzWb4zFrf?uid=6617213711&rl=0&page=1"
    print(url)
    selector = handle_html(cookie,url)
    # 存放所有的转发人的id
    uri_list = []
    try:
        # //*[@id="M_"]/div[1]/a
        uid = selector.xpath('//*[@id="M_"]/div[1]/a[1]/@href')[0][1:]
        # 查找有没有转发
        format_str = selector.xpath('//*[@id="rt"]/text()')
        format_num = re.findall(r"(?<=\[)\d+(?=\])", format_str[0])
        if len(format_num) == 0:
            print("无转发人")
            return uri_list
        print("format_num: ",format_num)
        # 查找转发页数
        try:
            page_num_str = selector.xpath('//*[@id="pagelist"]/form/div/text()')
            page_num_str = page_num_str[-1].split("/")[-1]
            page_num = re.findall(r"\d+",page_num_str)[-1]
            print("page num :",page_num)
        except:
            print("一页")
            page_num = 1
        total = 0
        # 遍历每一页，查找微博id和转发人的id
        for i in range(1,int(page_num)+1):
            url_page = "https://weibo.cn/repost/"  + weiboid + "?uid=" + uid + "&page=" + str(i)
            print(url_page)
            selector = handle_html(cookie, url_page)
            weio_id = selector.xpath('//span[@class="cc"]/a/@href')
            uri = selector.xpath('//span[@class="cc"]/../a[1]/@href')
            # print(uri)
            # print(uri[0][1:])
            for j in range(len(weio_id)):
                children_tree = {}

                uid = uri[j][1:]
                wid = weio_id[j].split("/")[2]
                children_tree["weibo id"] = wid
                children_tree["user id"] = uid
                children_tree["children"] = find_forward_new(wid)
                uri_list.append(children_tree)
            total = total + len(weio_id)
            time.sleep(2)
        return uri_list
    except:
        print("未找到{}的转发树".format(url))
        return uri_list


# if __name__ == '__main__':
def structure_tree(weibo_id,writer_path):
    # 转发树，一个微博id对应若干个转发人的id
    forward_tree = {}
    forward_tree["type"] = "tree"
    # 转发队列，存储将要查询的转发对（微博id和用户id，用这两个字段构建网址）
    # weibo_id = "LAGuj9Fzd"
    # uid = "7583190896"
    children_tree = {}
    children_tree["weibo id"] =  weibo_id
    children_tree["user id"] = get_uid(weibo_id)
    children_tree["children"] = find_forward_new(weibo_id)
    forward_tree["data"] = children_tree
    writer_path = writer_path + "/forward"
    if not os.path.exists(writer_path):
        os.makedirs(writer_path)
    writer_path = writer_path + "/" + weibo_id +".json"
    with open(writer_path, "w", encoding='utf-8') as f:  ## 设置'utf-8'编码
        f.write(json.dumps(forward_tree, indent=4,ensure_ascii=False))



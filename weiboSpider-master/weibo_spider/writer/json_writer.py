import codecs
import json
import logging
import os

from .writer import Writer

logger = logging.getLogger('spider.json_writer')


class JsonWriter(Writer):
    def __init__(self, file_path):
        self.file_path = file_path

    def write_user(self, user):
        self.user = user

    def _update_json_data(self, data, weibo_info):
        """更新要写入json结果文件中的数据，已经存在于json中的信息更新为最新值，不存在的信息添加到data中"""
        data['user'] = self.user.__dict__
        if data.get('weibo'):
            is_new = 1  # 待写入微博是否全部为新微博，即待写入微博与json中的数据不重复
            for old in data['weibo']:
                if weibo_info[-1]['id'] == old['id']:
                    is_new = 0
                    break
            if is_new == 0:
                for new in weibo_info:
                    flag = 1
                    for i, old in enumerate(data['weibo']):
                        if new['id'] == old['id']:
                            data['weibo'][i] = new
                            flag = 0
                            break
                    if flag:
                        data['weibo'].append(new)
            else:
                data['weibo'] += weibo_info
        else:
            data['weibo'] = weibo_info
        return data

    def write_weibo(self, weibos):
        """将爬到的信息写入json文件"""
        data = []
        # if os.path.isfile(self.file_path):
        #     with codecs.open(self.file_path, 'r', encoding='utf-8') as f:
        #         data = json.load(f)

        # data = self._update_json_data(data, [w.__dict__ for w in weibos])
        # data_writer = []
        for v in [w.__dict__ for w in weibos]:
            data_one = {}
            data_one['情报源'] = self.user.__dict__['nickname']
            data_one['情报源注册时长'] = ''
            data_one['情报源关注者数目'] = self.user.__dict__['following']
            data_one['文章标题'] = v['title']
            data_one['转自何处'] = ''
            data_one['文章作者'] = self.user.__dict__['nickname']
            data_one['文章发布时间'] = v['publish_time']
            data_one['爬取时间'] = v['spider_time']
            data_one['文章正文'] = v['content']
            data_one['阅读数'] = ''
            data_one['点赞数'] = v['up_num']
            data_one['转发数'] = v['retweet_num']
            data_one['评论数'] = v['comment_num']
            data_one['链接'] = v['article_url']
            # print(data_one)
            data.append(data_one)
        #data.append(data_writer)
        with codecs.open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
        logger.info(u'%d条微博写入json文件完毕，保存路径：%s', len(weibos), self.file_path)

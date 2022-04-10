# 导入模板模块
from flask import Flask, jsonify, request
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from absl import app, flags
from weibo_spider import spider
import os
# Flask相关变量声明

flask_app = Flask(__name__)
flask_app.config.update(
    DEBUG=True
)
# 跨域问题
CORS(flask_app, supports_credentials=True)


@flask_app.route('/weibo', methods=["post", "get"])
def mil():
    # keys = request.form.get("key")  # 调用者传参 ky
    # 请求进来 输入爬取内容
    # taobao_details.get_detail(keys)#这里就是你的爬虫程序接入口
    # 爬虫程序
    app.run(spider.main)
    return "mil_ok"  # jsonify({"code": 1})


@flask_app.route('/weibo/search', methods=["post", "get"])
def mil_keyword():
    keys = request.form.get("key")  # 调用者传参 ky
    # 请求进来 输入爬取内容
    # taobao_details.get_detail(keys)#这里就是你的爬虫程序接入口
    # 爬虫程序
    keys = "中国"
    cmd = 'python -m weibo_spider' + ' ' + keys
    os.system(cmd)
    # app.run(spider.search_keyword(keys))
    return "mil_ok"  # jsonify({"code": 1})

if __name__ == '__main__':
    flask_app .run(port=5555, debug=True, host='127.0.0.1')
    http_server = WSGIServer(('127.0.0.1', 5555), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
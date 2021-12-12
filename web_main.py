# encoding=utf8
from hashlib import sha1
from flask import Flask, request, abort, Response
import reply
import receive
import requests
import json
import time

app = Flask(__name__)


def wu_dao_generate(query):
    '''
    悟道文本生成
    '''
    API_KEY = "mAmIxX/F45vUpL99X0aBitZMN3WOsafVJgYDdI0dSkql+ouHEsMcTg=="  # 从悟道开发平台获取
    API_SECRET = "ajF+8ga8fJq3670bq3yprgFZ9k9Ehlfza8Va7AFkCuCZClvPP0DWFg=="
    KEY = "queue2"  # 队列名称，默认queue1
    # CONTENT = "问题：程序员情商高吗？答案："  # 文本内容
    CONTENT = "问题：" + query + "答案："  # 文本内容
    CONCURRENCY = 10  # 并发数
    TYPE = "sentence"  # para,sentence
    request_url = "https://pretrain.aminer.cn/api/v1/"
    api = 'generate'

    # 指定请求参数格式为json
    headers = {'Content-Type': 'application/json'}
    request_url = request_url + api
    data = {
        "key": KEY,
        "content": CONTENT,
        "concurrency": CONCURRENCY,
        "type": TYPE,
        "apikey": API_KEY,
        "apisecret": API_SECRET
    }
    response = requests.post(request_url, headers=headers, data=json.dumps(data))
    if response:
        while "output" not in response.json()["result"]:
            time.sleep(10)
            response = requests.get(request_url)
        output = response.json()["result"]["output"]
        answer = ""
        for index, content in enumerate(output):
            if index != len(output):
                answer += str(index) + "." + content[0] + "\n"
            else:
                answer += str(index) + "." + content[0]
        return answer
    else:
        return "悟道生成失败"


def verification_token(request):
    token = "Token"
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    list = [token, timestamp, nonce]
    list.sort()
    list_str = "".join(list)
    hashcode = sha1(list_str.encode('utf8')).hexdigest()
    if hashcode != signature:
        abort(403)
    else:
        if request.method == "GET":
            echostr = request.args.get('echostr')
            if not echostr:
                abort(400)
            return echostr
        elif request.method == "POST":
            try:
                xml_str = request.data
                print("Post wx_data is: ", xml_str)
                rec_msg = receive.parse_xml(xml_str)
                if isinstance(rec_msg, receive.Msg):
                    to_user = rec_msg.FromUserName
                    from_user = rec_msg.ToUserName
                    if rec_msg.MsgType == "text":
                        # content = rec_msg.Content.decode('utf-8')
                        content = wu_dao_generate(rec_msg.Content.decode('utf-8'))
                        reply_msg = reply.TextMsg(to_user, from_user, content)
                        return reply_msg.send()
                    if rec_msg.MsgType == "image":
                        mediaId = rec_msg.MediaId
                        reply_msg = reply.ImageMsg(to_user, from_user, mediaId)
                        return reply_msg.send()
                    else:
                        return reply.Msg().send()
                else:
                    print("暂且不处理")
                    return "success"
            except Exception:
                return ""
        else:
            print("暂且不处理")
            return "success"


@app.route('/ner', methods=['post', 'get'])
def interactive_with_wx():
    result = verification_token(request)
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

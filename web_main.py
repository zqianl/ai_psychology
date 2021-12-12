# encoding=utf8
from hashlib import sha1
from flask import Flask, request, abort, Response
import reply
import receive

app = Flask(__name__)


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
                if isinstance(rec_msg, receive.Msg) and rec_msg.MsgType == 'text':
                    to_user = rec_msg.FromUserName
                    from_user = rec_msg.ToUserName
                    content = "test"
                    reply_msg = reply.TextMsg(to_user, from_user, content)
                    return reply_msg.send()
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

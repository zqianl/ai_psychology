# encoding=utf8
from hashlib import sha1
from flask import Flask, request

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
    if hashcode == signature:
        return echostr
    else:
        return ""


@app.route('/ner', methods=['post', 'get'])
def index():
    result = verification_token(request)
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

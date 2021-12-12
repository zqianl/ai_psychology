# encoding=utf8
from flask import Flask, request

app = Flask(__name__)


@app.route('/ner', methods=['post', 'get'])
def index():
    query = request.args.get('query')
    return str(query)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

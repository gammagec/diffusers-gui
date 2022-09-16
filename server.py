import os

from flask import Flask, Response, send_from_directory

app = Flask(__name__, static_url_path='', static_folder='app/dist/app')
app.config.from_object(__name__)

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/', methods=['GET'])
def index():
    content = get_file('app/dist/app/index.html')
    return Response(content, mimetype="text/html")

if __name__ == '__main__':
    app.run(port=80)
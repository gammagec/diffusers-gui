import base64, argparse, os
from io import BytesIO
from tkinter import W
from diffusers_gui.services import diffusers_service

from flask import Flask, Response, jsonify, request
from flask_cors import CORS, cross_origin
from diffusers_gui import DiffusersService, Config, Namespace

app = Flask(__name__, static_url_path='', static_folder='app/dist/app')
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

diffusers_service = DiffusersService()

parser = argparse.ArgumentParser()

parser.add_argument(
    "--config",
	type=str,
	nargs="?",
	default="config/config.yaml",
	help="the config file to use"
)

opt = parser.parse_args()
config = Config()
config.load(opt.config)

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

@app.route('/api/txt2img', methods=['GET'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def txt2img():
    print(f'doing txt2img')

    prompt = request.args.get('prompt')
    seed = int(request.args.get('seed'))
    steps = int(request.args.get('steps'))
    height = int(request.args.get('height'))
    width = int(request.args.get('width'))
    downsampling = int(request.args.get('downsampling'))
    scale = float(request.args.get('scale'))
    image = diffusers_service.run_txt2img(
        '',
        seed,
        steps,
        1, 1, # n_iter and batch
        prompt,
        0.0, # eta steps
        height, width,
        3, # channels
        downsampling,
        scale,
        '',
        embeddings=config.embeddings,
    )
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    print(f'returning image of size {image.size}')
    resp = jsonify(
        {
            'image': str(base64.b64encode(buffered.getvalue())),
        })
    return resp

if __name__ == '__main__':
    app.run(port=80)
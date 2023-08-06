__title__ = 'foyou-http'
__author__ = 'foyoux'
__version__ = '0.0.14'

import os
from datetime import datetime
from urllib.parse import urlparse

from flask import Flask, render_template, request, send_file, redirect
from flask_cors import CORS
from werkzeug.security import safe_join

app = Flask(__name__, static_url_path='/')
CORS(app, supports_credentials=True)


@app.get('/favicon.ico')
def favicon():
    return send_file(os.path.join(os.path.dirname(__file__), 'templates/favicon.ico'))


@app.post('/upload')
def upload():
    referer_url = request.args['url']
    path = safe_join(app.static_folder, urlparse(referer_url).path.strip('/'))
    for file in request.files.getlist('files'):
        s = os.path.join(path, file.filename)
        if os.path.exists(s):
            return f'<h1>{file.filename} 已存在</h1>'
        file.save(os.path.join(path, file.filename))
    return redirect(referer_url)


def pretty_size(size):
    if size < 1024:
        return f'{size} Byte'
    if size < (1024 * 1024):
        return '{:.2f} KB'.format(size / 1024)
    if size < (1024 * 1024 * 1024):
        return '{:.2f} MB'.format(size / (1024 * 1024))
    else:
        return '{:.2f} GB'.format(size / (1024 * 1024 * 1024))


# noinspection PyUnusedLocal
def index(e):
    path = safe_join(app.static_folder, request.path.strip('/'))
    if not os.path.exists(path):
        return render_template('404.html'), 400
    body = []
    f: os.DirEntry
    for f in os.scandir(path):
        if f.name.startswith('.'):
            continue
        f_stat = f.stat()
        body.append({
            'path': f.name + ('/' if f.is_dir() else ''),
            'time': datetime.strftime(datetime.fromtimestamp(f_stat.st_mtime), '%Y-%m-%d %H:%M:%S'),
            'size': pretty_size(f_stat.st_size) if f.is_file() else '-'
        })
    body.sort(key=lambda x: x['path'])
    body.sort(key=lambda x: not x['path'].endswith('/'))
    return render_template('index.html', title=request.path, body=body)


app.register_error_handler(404, index)


def start_server(host, port, dir_):
    app._static_folder = os.path.abspath(dir_)
    app.run(host=host, port=port)


def main():
    import argparse
    epilog = f'%(prog)s({__version__}) by foyoux(https://github.com/foyoux/foyou-http)'
    parser = argparse.ArgumentParser(prog='pyhttp', description='simple http server for share files.', epilog=epilog)
    parser.add_argument('-v', '--version', action='version', version=epilog)

    parser.add_argument('dir', nargs='?', default='.', help='HTTP Server 共享目录')
    parser.add_argument('--host', dest='host', default='0.0.0.0', help='HTTP Server 监听地址')
    parser.add_argument('--port', dest='port', default='5512', help='HTTP Server 监听端口')
    args = parser.parse_args()

    start_server(args.host, args.port, args.dir)


if __name__ == '__main__':
    start_server('0.0.0.0', '1234', '/')

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from module import get_hashtags
import time, json

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '123123secret'
app.config['HOST'] = '0.0.0.0'

io = SocketIO(app)

last_run = time.time()

@io.on('message')
def handle_message(data):
    global last_run
    print(f'Frontend Response: {data}')

@io.on('post-emit')
def handle_post(data):
    # print(data['data'])
    time.sleep(2)
    hashtags=list(set(get_hashtags(data['data'])))
    print(hashtags)
    emit('post-emit', json.dumps(hashtags), json=True)


@app.get('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    io.run(app)
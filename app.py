import os
import flask
import flask_socketio

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

app = flask.Flask(__name__)

@app.route('/')
def hello():
    return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    }) 

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')


@socketio.on('new input')
def on_new_number(data):
    print("Got an event for new input:", input)
    newinput = data['input']
    socketio.emit('input received', {
        'input': newinput
    })

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
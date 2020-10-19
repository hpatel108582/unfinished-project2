import os
import flask
import flask_socketio
import flask_sqlalchemy
from os.path import join, dirname
from dotenv import load_dotenv
import json
import models 





dotenv_path = join(dirname(__file__), 'pro2.env')
load_dotenv(dotenv_path)



MESSAGES_RECEIVED_CHANNEL= 'messages received'

app = flask.Flask(__name__)

nameList=[]
nameCounter=0
liveCounter=0

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")



database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()


def emit_all_messages(channel):
    all_messages = [ \
       ( db_message.name,db_message.message)  for db_message \
        in db.session.query(models.Users).all()]
        
    socketio.emit(channel, {
        'allMessages': all_messages
    })

@app.route('/')
def hello():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    return flask.render_template('index.html')


@socketio.on('connect')
def on_connect():
    liveCounter=0
    liveCounter+=1
    print("Live counter: ", liveCounter)
    socketio.emit('connected', {
        'test': 'Connected'
    })
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')


@socketio.on('new message')
def on_new_number(data):
    response = data['response']
    print("Got an event for new message with data:", data)
    message = data['message']
    name=response['profileObj']['name']
    imgurl = response['profileObj']['imageUrl']
    
    db.session.add(models.Users(name,message));
    db.session.commit();
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    botMessage=""
    currentUserCounter=0
    updateUserCounter = int(data['userCount'])
    if (currentUserCounter!= updateUserCounter):
        currentUserCounter=updateUserCounter
        countUser="Users in the chat:  " + data['userCount']
    else:
        countUser=""
    
    ###########################################################
    
    if "!! help" in message:
        botMessage="Charles the bot: commands are-> !! about, !! funtranslate <input> "
    elif "!! about" in message:
        botMessage="Charles the bot: Hi im Charles. I am a bot. Please be nice and treat me like a human :)"
    ###########################################################
    print("People talking in the chat: ", nameCounter)
    socketio.emit('message received', {
        'message': message,
        'name': name,
        'botMessage': botMessage,
        'userCount':countUser
        
    })
@socketio.on('new google json')
def new_response(data):
    
    response = data['response']
    print(response['profileObj']['imageUrl'])
    print(response['profileObj']['name'])

if __name__ == '__main__':
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
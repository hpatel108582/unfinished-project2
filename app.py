import os
import flask
import flask_socketio
import flask_sqlalchemy
from os.path import join, dirname
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate
import json
import models 




dotenv_path = join(dirname(__file__), 'pro2.env')
load_dotenv(dotenv_path)

googleApi=[ 
    os.environ['type'],
    os.environ['project_id'],
    os.environ['private_key_id'],
    os.environ['private_key'],
    os.environ['client_email'],
    os.environ['client_id'],
     os.environ['auth_uri'],
     os.environ['token_uri'],
     os.environ['auth_provider_x509_cert_url'],
     os.environ['client_x509_cert_url']
     ]

googleCall= [{
  "type": googleApi[0],
  "project_id": googleApi[1],
  "private_key_id": googleApi[2],
  "private_key": googleApi[3],
  "client_email": googleApi[4],
  "client_id": googleApi[5],
  "auth_uri": googleApi[6],
  "token_uri": googleApi[7],
  "auth_provider_x509_cert_url": googleApi[8],
  "client_x509_cert_url": googleApi[9]
}]


os.environ['GOOGLE_APPLICATION_CREDENTIALS']=json.dumps(googleCall)

MESSAGES_RECEIVED_CHANNEL= 'messages received'

app = flask.Flask(__name__)

nameList=[]
nameCounter=0
liveCounter=0

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


dbuser = os.environ['USER']


database_uri= os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()

def emit_all_messages(channel):
    all_messages = [ \
        db_message.message for db_message \
        in db.session.query(models.Messanger).all()]
        
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
    
    print("Got an event for new message with data:", data)
    message = data['message']
    name=data['name']
    db.session.add(models.Messanger(data['message']));
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
    
    translate_client = translate.Client()
    ###########################################################
    if "!! funtranslate"  in message:
        getMessage = message.split()
        newMessage=""
        newMessList=getMessage[2:]
        for i in range(0,len(getMessage[2:])):
            newMessage+=newMessList[i]+ " "
        output = translate_client.translate( newMessage, target_language='ja')
        botMessage="Charles the bot: " + output['translatedText']
    elif "!! help" in message:
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


if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
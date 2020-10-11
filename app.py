import os
import flask
import flask_socketio
from os.path import join, dirname
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate
import json

dotenv_path = join(dirname(__file__), 'pro2.env')
load_dotenv(dotenv_path)

os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/home/ec2-user/environment/lect8-react/google.json"


app = flask.Flask(__name__)

nameList=[]
nameCounter=0
liveCounter=0

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")



@app.route('/')
def hello():
    return flask.render_template('index.html')


@socketio.on('connect')
def on_connect():
    liveCounter=0
    liveCounter+=1
    print("Live counter: ", liveCounter)
    socketio.emit('connected', {
        'test': 'Connected'
    })

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')


@socketio.on('new message')
def on_new_number(data):
    print("Got an event for new message with data:", data)
    message = data['message']
    name=data['name']
    nameCounter=0
    botMessage=""
    translate_client = translate.Client()
    
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
    if name not in nameList:
        nameList.append(name)
        nameCounter+=1
    print("People talking in the chat: ", nameCounter)
    socketio.emit('message received', {
        'message': message,
        'name': name,
        'botMessage': botMessage
        
    })


if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
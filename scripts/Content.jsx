
import React, {useState,useEffect} from 'react';
import { Socket } from './Socket';
import './style.css'; 
import TextField from '@material-ui/core/TextField'   // styling purpose



 var users = [];
    var countUsers=0;

export function Content() {
    
    const [state, setState] = useState ({message: '', name: '',botmessage: '',userCount:''})
    const [chat, setChat] = useState ([])
    const [messages, setMessages] = React.useState([]);
  
         function newMessage() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log("Received an message from server: " + data['message'] + " from " + data['name'] +
                " and bot said: "+ data['botMessage']);
                
                setChat([...chat,[data['name'] +" : ",data['message']], data['botMessage'],data['userCount']])
                
                
            })
        });
    }
    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('messages received', (data) => {
                setMessages(data['allMessages']);
            })
        });
    }
    
    getNewMessages();
    
    newMessage();
        

  
    const onTextChange = e => {
      setState ({...state, [e.target.name]: e.target.value})
      console.log(e.target.name,e.target.value)
    }
    
    const onMessageSubmit = (e) => {
      e.preventDefault()
      const {name, message } =state
     
      if  (users.includes(name)!=true)
      {
          users.push(name)
          ++countUsers;
      }
      Socket.emit('new message', {
        'name': name,
        'message': message,
        'userCount': (countUsers).toString()
    });
      setState({message: '', name: ''})
    }
    

    
  
    
 
  return (
    <body>
    <div className="card">
    <form onSubmit={onMessageSubmit}>
      <h2> SENDER </h2>
      <div className="name-field">
        <TextField 
          name="name" 
          onChange={ e=> onTextChange(e)} 
          value={state.name} 
          label = "Name" 
          />
          <p> Talk to Charles the bot! </p> 
          <p> Commands: !! help, !! about </p>
      </div>
      <div>
        <TextField 
          name="message" 
          onChange={ e=> onTextChange(e)} 
          value={state.message} 
          id="outline-multiline-static"  //This is for styling purposes
          variant = "outlined"
          label = "Message" 
          />
      </div>
     <button>Send Message </button>
    </form>
      <div className= "render-chat">
        <h2> CHAT </h2>
        <ol>
                    {messages.map((message, index) =>
                        <p key={index}>{message}</p>)}
                </ol>
         {chat.length > 0 &&
          chat.map(msg=> (
            <div>
              <p> {msg} </p>
            </div>
          ))}
      </div>
    </div>
    </body>
    
  );
}

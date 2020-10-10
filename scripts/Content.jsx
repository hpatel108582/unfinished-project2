
import React, {useState,useEffect} from 'react';
import { Socket } from './Socket';
import './style.css'; 
import TextField from '@material-ui/core/TextField'   // styling purpose
 
const init = []
 

export function Content() {
    
    const [state, setState] = useState ({message: '', name: ''})
    const [chat, setChat] = useState ([])
    
    
         function newNumber() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log("Received an message from server: " + data['message'] + " from " + data['name']);
                setChat([...chat,data['name'], data['message']])
            })
        });
    }
    
    newNumber();
        
        // setChat([...chat,{name, message}])
    
    
    const onTextChange = e => {
      setState ({...state, [e.target.name]: e.target.value})
      console.log(e.target.name,e.target.value)
    }
    
    const onMessageSubmit = (e) => {
      e.preventDefault()
      const {name, message } =state
      Socket.emit('new message', {
        'name': name,
        'message': message
    });
      setState({message: '', name: '' })
    }
    
    // const renderChat = () => {
      
    //   return chat.map(msg => ( 
        
    //     <div key={msg.id}>
    //       <h3> {msg.name} : <span> {msg.message} </span>  
    //       </h3>
    //     </div>
        
    //     ))
    // }
    const renderChat = () => {
      return chat.map(({ name, message}, index) => (
        <div key={index}>
          <h3> 
            {name}: <span> {message} </span>
            </h3>
          </div>
        ))
    }
    
    
 
  return (
    <div className="card">
    <form onSubmit={onMessageSubmit}>
      <h1> Messanger </h1>
      <div className="name-field">
        <TextField 
          name="name" 
          onChange={ e=> onTextChange(e)} 
          value={state.name} 
          label = "Name" 
          />
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
        <h1> Chat log </h1>
        {renderChat()}
      </div>
    </div>
  );
}
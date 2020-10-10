
import React, {useState,useEffect} from 'react';
import { Socket } from './Socket';
import './style.css'; 
import TextField from '@material-ui/core/TextField'   // styling purpose
 
const init = []
 

export function Content() {
    
    const [messages,setMessages] = useState(["Hello and Welcome"]);
    const [message,setMessage]=useState("");
    
    
         function newNumber() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log("Received an message from server: " + data['message']);
                setMessages([...messages,data['message']]);
            })
        });
    }
    
    newNumber();
    
    
    const onChange = e => {
      setMessage(e.target.value);
    }
    
    const onClick = () => {
      if (message !== "")
      {
        Socket.emit('new message', {
        'message': message,
    });
        setMessage("");
      } else {
         alert("Please Add a Message");
      }
    }
    

    
    
 
  return (
    <div >
        {messages.length > 0 &&
          messages.map(msg=> (
            <div>
              <p> {msg} </p>
            </div>
          ))}
        <input value={message} name="message" onChange={e => onChange(e)} />
        <button onClick={ ()=> onClick ()} > Send Message </button> 
        
    </div>
  );
}
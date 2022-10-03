
import './App.css'

import React, { useState, useEffect } from 'react';
import {io}  from "socket.io-client";

const ENDPOINT = 'http://localhost:8000';
const socket = io(ENDPOINT, {
  autoConnect: true,
   auth: {
    token: 'my_token'
   },
});


function App() {
  const [isConnected, setIsConnected] = useState(socket.connected);
  const [lastPong, setLastPong] = useState(null);
  const [event, setEvent] = useState(null);

  console.log("data", event);

  useEffect(() => {
    socket.on('connect', () => {
      setIsConnected(true);
    });

    socket.on('disconnect', () => {
      setIsConnected(false);
    });

    socket.on('pong', () => {
      setLastPong(new Date().toISOString());
    });
    
    socket.on('my_event', (data) => {
      console.log("my_event", data)
      setEvent(data);
    });

   

    socket.emit('my_event', {data: ''}, {token: 'my_token'});

    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('pong');
    };
  }, [setEvent]);

  // setInterval(() => {
  //  socket.off('disconnect');

  // }, 1000);

  const sendPing = () => {
    socket.emit('ping');
  }
  const sendEvent = () => {
    // socket.emit('my_event', {data: "hello"})
    //  send with auth token
    socket.emit('my_event', {data: "hello"}, {token: ''})
  }
  

  return (
 <div>
      <p>Connected: { '' + isConnected }</p>
      <p>Last pong: { lastPong || '-' }</p>
      <p>My Event: {}</p>
      <button onClick={ sendEvent }>Send ping</button>
    </div>
  )
}

export default App

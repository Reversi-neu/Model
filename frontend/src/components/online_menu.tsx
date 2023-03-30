import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { socket } from '../services/socket';

export function OnlineMenu() {

    // const [isConnected, setIsConnected] = useState(socket.connected);
    // const [fooEvents, setFooEvents] = useState([]);
  
    // useEffect(() => {
    //   function onConnect() {
    //     setIsConnected(true);
    //   }
  
    //   function onDisconnect() {
    //     setIsConnected(false);
    //   }
  
    //   socket.on('connect', onConnect);
    //   socket.on('disconnect', onDisconnect);
  
    //   return () => {
    //     socket.off('connect', onConnect);
    //     socket.off('disconnect', onDisconnect);
    //   };
    // }, []);

    return (
        <div className="App">
            <header className="App-header" style={{padding: '40px 0'}}>
                <p>Online Play</p>
            </header>
            <div className="App-body">
                <Link to="/play/online">Search For Lobby</Link>
                {/* <ConnectionManager />
                <p>State: { '' + isConnected }</p> */}
            </div>
        </div>
    );
}

function ConnectionManager() {
    function connect() {
      socket.connect();
    }
  
    function disconnect() {
      socket.disconnect();
    }
  
    return (
      <>
        <button onClick={ connect }>Connect</button>
        <button onClick={ disconnect }>Disconnect</button>
      </>
    );
  }
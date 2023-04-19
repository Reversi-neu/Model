import { Slider } from "@mui/material";
import React from "react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useToken } from "../hooks/use_token";
import { socket } from '../services/socket';
import { createGame } from "../services/game_service";
import { toast, ToastContainer } from "react-toastify";

// Online menu component, shows online lobby + search
export function OnlineMenu() {

    const {token} = useToken();
    const [isConnected, setIsConnected] = useState(socket.connected);
    const [isSearching, setIsSearching] = useState(false);
    const [size, setSize] = React.useState<number>(8);
  
    useEffect(() => {
      function onConnect() {
        setIsConnected(true);
      }
  
      function onDisconnect() {
        setIsConnected(false);
      }
  
      socket.on('connect', onConnect);
      socket.on('lobbyFound', foundLobby);
      socket.on('disconnect', onDisconnect);
      socket.connect();
  
      return () => {
        if (socket.connected) socket.disconnect();
        socket.off('connect', onConnect);
        socket.off('lobbyFound', foundLobby);
        socket.off('disconnect', onDisconnect);
      };
    }, []);

    const searchForLobby = () => {
        socket.emit('searchForLobby', {id: token, size: size});
        setIsSearching(true);
    }

    const foundLobby = (data: any) => {
        console.log(data);
        if (data.player1.userID === token || data.player2.userID === token) {
            window.location.href = `/play/online/${data.id}`;
        }
    }

    return (
        <div className="App">
            <header className="App-header" style={{padding: '40px 0'}}>
                <p>Online Play</p>
            </header>
            <div className="App-body">
                {
                    isSearching ?
                        <div>
                            <p style={{margin: '0 0 20px 0'}}>Searching...</p>
                            <a onClick={() => {
                                socket.emit('cancelLobbySearch', {id: token});
                                setIsSearching(false);
                            }}>Cancel</a>
                        </div>
                    :
                        <>
                            <span style={{
                                display: 'flex', 
                                flexDirection: 'column', 
                                alignItems:'flex-start',
                                margin: '0 20px'
                            }}>
                                <label style={{fontSize: '0.5em'}}>Size: {size}</label>
                                <Slider
                                    aria-label="Size"
                                    defaultValue={8}
                                    value={size}
                                    step={2}
                                    marks
                                    min={4}
                                    max={32}
                                    onChange={(event, value) => {
                                        setSize(value as number);
                                    }}
                                    style={{
                                        width: 'fit-content',
                                        minWidth: '300px',
                                    }}
                                />
                            </span>
                            <a 
                                style={{ textDecoration: 'none' }}
                                onClick={() => searchForLobby()}
                            >
                                Search For Lobby
                            </a>
                            <hr style={{width: '100%'}}/>
                            <Link to="/play/online">View Ongoing Games</Link>
                        </>
                }
            </div>
            <ToastContainer theme="dark" />
        </div>
    );
}
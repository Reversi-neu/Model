import "../App.scss"
import { useToken } from "../hooks/use_token";
import { Link, useParams } from "react-router-dom";
import { GameType } from "./board/board";
import { getGamesByType, getGamesByTypeByUserID, createGame } from "../services/game_service";
import React from "react";
import Slider from '@mui/material/Slider';
import { toast, ToastContainer } from "react-toastify";

export function LobbyManager() {
    const { token } = useToken();
    const { gameType } = useParams<{gameType: string}>() as {gameType: GameType};
    const [size, setSize] = React.useState<number>(8);
    const [aiDifficulty, setAIDifficulty] = React.useState<number>(1);
    const [games, setGames] = React.useState<any[]>([]);

    React.useEffect(() => {
        handleLobbyRefresh();
    }, [gameType, token]);

    const handleLobbyRefresh = async () => {
        getGamesByTypeByUserID(gameType, token).then((games) => {
            console.log(games)
            setGames(games);
        });
    }

    const handleCreateGame = async () => {
        await createGame({
            player1ID: token,
            player2ID: 9,
            gameType: gameType,
            size: size,
            difficulty: aiDifficulty,
        });
        handleLobbyRefresh();
        toast.success('Game created!');
    };

    return (
        <div className="App">
            <header className="App-header" style={{fontSize: '5em'}}>
                <p>{ gameType.toLocaleUpperCase() }</p>
            </header>
            <div className="App-body">
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}>
                    {
                        games.map((game) => {
                            return (
                                <div 
                                    style={{
                                        display: 'flex',
                                        flexDirection: 'row',
                                        alignItems: 'center',
                                        justifyContent: 'space-between',
                                        width: '100%',
                                        padding: '10px 20px',
                                        border: '1px solid black',
                                        borderRadius: '5px',
                                        background: '#22262e',
                                        // boxShadow: '0 0 1px #c4c4c4',
                                        margin: '5px',
                                    }}
                                    key={game.id}
                                >
                                    {
                                        (gameType === 'ai' || gameType === 'local') ?
                                        <p>
                                            <u>{ game.player1.username || ('Guest' + game.player1.userID) }</u> <em>vs. </em> 
                                            {
                                                gameType === 'ai' ?
                                                <u>{ 'AI-' + (game.difficulty > 0 && game.difficulty) }</u>
                                                :
                                                <u>LOCAL</u>
                                            }
                                        </p>
                                        :
                                        <p>
                                            <u>{ game.player1.username || ('Guest' + game.player1.userID) }</u> <em>vs. </em>
                                            <u>{ game.player2.username || ('Guest' + game.player2.userID) }</u>
                                        </p>
                                    }
                                    <p>{ game.size } x { game.size }</p>
                                    <Link to={`/play/${game.type}/${game.id}`}>
                                        Join
                                    </Link>
                                </div>
                            )
                        })
                    }
                    <div style={{
                        display: 'flex',
                        flexDirection: 'row',
                        margin: '20px',
                    }}>
                        <button onClick={handleLobbyRefresh}>
                            Refresh
                        </button>
                    </div>
                </div>
                
                <div style={{
                    display: gameType === 'online' ? 'none' : 'flex',
                    margin: '20px',
                    padding: '20px',
                    justifyContent: 'center',
                    border: '1px solid #c4c4c4',
                    boxShadow: '0 0 5px #c4c4c4',
                    borderRadius: '15px',
                    width: '100%',
                    background: '#22262e',
                }}>
                    <span style={{
                            display: 'flex', 
                            flexDirection: 'column', 
                            alignItems:'flex-start',
                            margin: '0 20px'
                        }}
                    >
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

                    {
                        gameType === 'ai' &&
                        <span style={{
                                display: 'flex', 
                                flexDirection: 'column', 
                                alignItems:'flex-start',
                                margin: '0 20px'
                            }}
                        >
                            <label style={{fontSize: '0.5em'}}>Difficulty: {aiDifficulty}</label>
                            <Slider
                                aria-label="aiDifficulty"
                                defaultValue={3}
                                value={aiDifficulty}
                                step={1}
                                marks
                                min={1}
                                max={4}
                                onChange={(event, value) => {
                                    setAIDifficulty(value as number);
                                }}
                                style={{
                                    width: 'fit-content',
                                    minWidth: '200px',
                                }}
                            />
                        </span>
                    }
                    
                    <button onClick={handleCreateGame}>
                        Create { gameType === 'local' || gameType === 'ai' ? 'Game' : 'Lobby'}
                    </button>
                </div>
            </div>
            <ToastContainer theme="dark" />
        </div>
    );
}
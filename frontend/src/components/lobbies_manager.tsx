import "../App.scss"
import { useToken } from "../hooks/use_token";
import { useParams } from "react-router-dom";
import { GameType } from "./board/board";
import { getGamesByType } from "../services/game_service";

export function LobbyManager() {
    const { token } = useToken();
    const { gameType } = useParams<{gameType: string}>() as {gameType: GameType};
    const games: any[] = [];

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
                                <div style={{
                                    display: 'flex',
                                    flexDirection: 'row',
                                    alignItems: 'center',
                                    justifyContent: 'space-between',
                                    width: '100%',
                                    padding: '10px',
                                    border: '1px solid black',
                                    borderRadius: '5px',
                                    margin: '10px',
                                }}>
                                    <div>
                                        <p>{ game.player1 }</p>
                                        <p>{ game.player2 }</p>
                                        <button>
                                            Join
                                        </button>
                                    </div>
                                </div>
                            )
                        })
                    }
                    <div style={{
                        display: 'flex',
                        flexDirection: 'row',
                    }}>
                        <button>
                            { gameType === 'local' || gameType === 'ai' ? 'Create ' : 'Search for '}
                            Game
                        </button>

                        <button>
                            Refresh
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
import "../App.scss"
import { useToken } from "../hooks/use_token";
import { useParams } from "react-router-dom";
import { GameType } from "./board/board";

export function LobbyManager() {
    const { token } = useToken();
    const { gameType } = useParams<{gameType: string}>() as {gameType: GameType};
    console.log(gameType)

    return (
        <div className="App">
            <header className="App-header" style={{fontSize: '5em'}}>
                <p>{ gameType.toLocaleUpperCase() }</p>
            </header>
            <div className="App-body">
                
            </div>
        </div>
    );
}
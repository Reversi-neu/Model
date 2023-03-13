import { Link } from "react-router-dom";

export function OnlineMenu() {
    return (
        <div className="App">
            <header className="App-header" style={{padding: '40px 0'}}>
                <p>Online Play</p>
            </header>
            <div className="App-body">
                <Link to="/play/online">Search For Lobby</Link>
            </div>
        </div>
    );
}
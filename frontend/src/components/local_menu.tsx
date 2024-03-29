import { Link } from "react-router-dom";

// LocalMenu component, shows the local menu with the options to play against AI or against another human(locally)
export function LocalMenu() {
    return (
        <div className="App">
            <header className="App-header" style={{padding: '40px 0'}}>
                <p>Local Play</p>
            </header>
            <div className="App-body">
                <Link to="/play/ai">Versus AI</Link>
                <Link to="/play/local">Versus Human</Link>
            </div>
        </div>
    );
}
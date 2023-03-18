import { Link } from "react-router-dom";
import "../App.scss"
import { useToken } from "../hooks/use_token";

export function Title() {
    const { token, setToken } = useToken();

    const handleLogout = () => {
        setToken(undefined);

        // redirect to home
        window.location.href = "/";
    }

    const handleGuestLogin = () => {
        setToken("guest");

        // redirect to home
        window.location.href = "/";
    }

    return (
        <div className="App">
            <header className="App-header" style={{padding: '40px 0'}}>
                <p>Reversi</p>
            </header>
            <div className="App-body">
                {
                    token &&
                    <>
                        <Link to="local">Play Local</Link>
                        <Link to="online">Play Online</Link>
                    </>
                }
                {
                    !token ?
                        <>
                            <a onClick={handleGuestLogin}>Play As Guest</a>
                            <Link to="login">Login</Link>
                        </>
                        :
                        <Link to="/" onClick={handleLogout}>Logout</Link>
                }
            </div>
        </div>
    );
}
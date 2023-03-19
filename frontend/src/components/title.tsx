import { Link } from "react-router-dom";
import "../App.scss"
import { useToken } from "../hooks/use_token";
import { signupGuest } from "../services/user_service";

export function Title() {
    const { token, setToken } = useToken();

    const handleLogout = () => {
        setToken(undefined);

        // redirect to home
        window.location.href = "/";
    }

    const handleGuestLogin = async () => {
        const token = await signupGuest();
        console.log(token)
        setToken(token.userID);

        // redirect to home
        // window.location.href = "/";
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
                            <Link to="login">Sign In</Link>
                        </>
                        :
                        <Link to="/" onClick={handleLogout}>Sign Out</Link>
                }
            </div>
        </div>
    );
}
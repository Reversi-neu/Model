import React from "react";
import "../App.scss"
import { useToken } from "../hooks/use_token";
import { getUserByID } from "../services/user_service";

// Settings component, shows the user info
export function Settings() {
    const { token, setToken } = useToken();
    const [username, setUsername] = React.useState("");
    const [password, setPassword] = React.useState("");

    React.useEffect(() => {
        getUserByID(token).then((user) => {
            setUsername(user.username);
            setPassword(user.password);
        });
    }, [token]);

    return (
        <div className="App">
            <header className="App-header" style={{padding: '40px 0'}}>
                <p>User Settings</p>
            </header>
            <div className="App-body">
                <div className="form">
                    <label htmlFor="username">Username</label>
                    <p> {username} </p>
                </div>
                <div className="form">
                    <label htmlFor="password">Password</label>
                    <p> {password} </p>
                </div>
            </div>
        </div>
    );
}
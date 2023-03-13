import React from 'react';
import { loginUser } from '../services/user_service';

interface State {
    username: string;
    password: string;
}
interface Props {
    token: string;
    setToken: (token: string) => void;
}

export class Login extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = {
            username: "",
            password: ""
        }
    }

    render(): React.ReactNode {
        const handleSubmit = async (e : any) => {
            console.log(e)
            e.preventDefault();

            const token = await loginUser({
                username: this.state.username,
                password: this.state.password
            });
            this.props.setToken(token);

            // redirect to home
            window.location.href = "/";
        }
        
        return(
            <div className="App">
                <header className="App-header">
                    <h1 style={{fontSize: '5rem'}}>Log In</h1>
                </header>
                <div className="App-body">
                    <form onSubmit={handleSubmit} style={{fontSize: '1rem'}}>
                        <div style={{margin: '20px 0'}}>
                            <p>Username</p>
                            <input type="text" onChange={e => this.setState({username: e.target.value})}/>
                        </div>
                        <div style={{margin: '20px 0'}}>
                            <p>Password</p>
                            <input type="password" onChange={e => this.setState({password: e.target.value})}/>
                        </div>
                        <div>
                            <button type="submit">Submit</button>
                        </div>
                    </form>
                </div>
            </div>
        )
    }
    
}
  
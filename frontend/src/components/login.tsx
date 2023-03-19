import React from 'react';
import { loginUser, signupUser } from '../services/user_service';  
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

interface State {
    username: string;
    password: string;
    passwordConfirm: string;
    signup: boolean;
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
            password: "",
            passwordConfirm: "",
            signup: false
        }
    }

    render(): React.ReactNode {
        const handleSubmit = async (e : any) => {
            e.preventDefault();

            if (this.state.signup) {
                if (this.state.password !== this.state.passwordConfirm) {
                    toast.error("Passwords do not match");
                    return;
                }

                const token = await signupUser({
                    username: this.state.username,
                    password: this.state.password
                });
                this.props.setToken(token.userID);

                // redirect to home
                window.location.href = "/";
            } else {
                const token = await loginUser({
                    username: this.state.username,
                    password: this.state.password
                });
                this.props.setToken(token.userID);

                // redirect to home
                window.location.href = "/";
            }
        }
        
        return(
            <div className="App">
                <header className="App-header">
                    <h1 style={{fontSize: '5rem'}}>Sign {this.state.signup ? 'Up' : 'In'}</h1>
                </header>
                <div className="App-body">
                    <form onSubmit={handleSubmit} style={{fontSize: '1rem', height: '220px'}}>
                        <div style={{margin: '20px 0'}}>
                            <p>Username</p>
                            <input type="text" onChange={e => this.setState({username: e.target.value})}/>
                        </div>
                        <div style={{margin: '20px 0'}}>
                            <p>Password</p>
                            <input type="password" onChange={e => this.setState({password: e.target.value})}/>
                        </div>
                        {
                            this.state.signup &&
                            <div style={{margin: '20px 0'}}>
                                <p>Confirm Password</p>
                                <input type="password" onChange={e => this.setState({passwordConfirm: e.target.value})}/>
                            </div>
                        }
                        <button type="submit">Submit</button>
                    </form>
                    <div  style={{margin: '40px', fontSize:'0.5em'}} onClick={() => this.setState({signup: !this.state.signup})}>
                        {
                            !this.state.signup 
                                ?
                            <a>Sign up Instead?</a>
                                :
                            <a>Sign in Instead?</a>
                        }
                    </div>
                </div>
                <ToastContainer theme="dark" />
            </div>
        )
    }
    
}
  
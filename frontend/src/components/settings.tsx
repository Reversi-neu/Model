import React from "react";
import "../App.scss"

interface State {}
interface Props {}

export class Settings extends React.Component<Props, State> {
    render(): React.ReactNode {
        return (
            <div className="App">
                <header className="App-header" style={{padding: '40px 0'}}>
                    <p>User Settings</p>
                </header>
                <div className="App-body">
                </div>
            </div>
        );
    }
}
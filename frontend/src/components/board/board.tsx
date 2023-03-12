import React from "react";
import './board.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGear } from '@fortawesome/free-solid-svg-icons';
import { CompactPicker, SketchPicker } from 'react-color';

interface State {
    gameType: GameType;
    board: number[][];
    winner: number; // 0 = no winner, 1 = player 1, 2 = player 2
    playerTurn: number; // 1 = player 1, 2 = player 2
    player1Color: string;
    player2Color: string;
    boardColor1: string;
    boardColor2: string;

    // ui stuff
    showSettings: boolean;
    rotateIcon: boolean;
}
interface Props {
    token: string;
}

export class Board extends React.Component<Props, State> {

    // example board, 8x8 with 1s and 2s in the middle "4" squares, 0s everywhere else
    exampleBoard = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 0, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ];

    constructor(props: Props) {
        super(props);
        this.state = {
            gameType: matchUrlToGameType(),
            board: this.exampleBoard,
            winner: 0,
            playerTurn: 1,
            player1Color: "#000000",
            player2Color: "#FFF",
            boardColor1: "#769656",
            boardColor2: "#eeeed2",
            // ui stuff
            showSettings: false,
            rotateIcon: false
        }
    }

    render(): React.ReactNode {
        return (
            <div className="App">
                <small>Type: {this.state.gameType.toLocaleUpperCase()}</small>
                <div className="board">
                    <table>
                        <tbody>
                        {
                            this.state.board.map((row, i) => {
                                return (
                                    <tr key={i}>
                                        {
                                            row.map((col, j) => {
                                                return (
                                                    <td key={j} style={{
                                                        backgroundColor: (i + j) % 2 === 0 ? this.state.boardColor1 : this.state.boardColor2,
                                                        borderColor: (i + j) % 2 === 0 ? this.state.boardColor2 : this.state.boardColor1,
                                                    }}>
                                                        {
                                                            col === 0 ? <div className="empty"/> 
                                                            : 
                                                            col === 1 ? 
                                                            <div className="player" style={{
                                                                backgroundColor: this.state.player1Color
                                                            }}/> 
                                                            :
                                                            col === 2 ? 
                                                            <div className="player" style={{
                                                                backgroundColor: this.state.player2Color
                                                            }}/> 
                                                            : 
                                                            null
                                                        }
                                                    </td>
                                                )
                                            })
                                        }
                                    </tr>
                                )
                            })
                        }
                        </tbody>
                    </table>
                    <div style={{
                        color: 'white',
                        margin: '10px',
                        fontSize: '2em',
                        cursor: 'pointer',
                        position: 'absolute',
                        top: '20px',
                        right: '0',
                    }}>
                        <FontAwesomeIcon 
                            className={ this.state.rotateIcon ? "rotate" : ""}
                            style={{ boxShadow: '0 0 10px 0 rgba(0,0,0,0.5)', borderRadius: '15px', padding: '10px', backgroundColor: '#282c34' }}
                            icon={faGear} 
                            onClick={() => this.setState({showSettings: !this.state.showSettings, rotateIcon: true})}
                            onAnimationEnd={() => this.setState({ rotateIcon: false })}
                        />
                        <div className="settings"
                            style={{ 
                                width: this.state.showSettings ? '250px' : '0px',
                                height: this.state.showSettings ? 'fit-content' : '0px',
                                opacity: this.state.showSettings ? '1' : '0',
                            }}
                        >
                            <span>
                                <label>Player 1 Color</label>
                                <CompactPicker
                                    color={ this.state.player1Color }
                                    onChangeComplete={ (color) => this.setState({ player1Color: color.hex }) }
                                />
                            </span>
                            <span>
                                <label>Player 2 Color</label>
                                <CompactPicker
                                    color={ this.state.player2Color }
                                    onChangeComplete={ (color) => this.setState({ player2Color: color.hex }) }
                                />
                            </span>
                            <span>
                                <label>Board Color 1</label>
                                <CompactPicker
                                    color={ this.state.boardColor1 }
                                    onChangeComplete={ (color) => this.setState({ boardColor1: color.hex }) }
                                />
                            </span>
                            <span>
                                <label>Board Color 2</label>
                                <CompactPicker
                                    color={ this.state.boardColor2 }
                                    onChangeComplete={ (color) => this.setState({ boardColor2: color.hex }) }
                                />
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export enum GameType {
    Online = "online",
    AI = "ai",
    Local = "local"
}

function matchUrlToGameType(): GameType {
    const url = window.location.pathname;
    const split = url.split("/");
    const gameType = split[split.length - 1];
    switch (gameType) {
        case GameType.Online:
            return GameType.Online;
        case GameType.AI:
            return GameType.AI;
        case GameType.Local:
            return GameType.Local;
        default:
            return GameType.Online;
    }
}
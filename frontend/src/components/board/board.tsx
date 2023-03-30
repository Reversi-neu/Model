import React from "react";
import './board.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGear } from '@fortawesome/free-solid-svg-icons';
import { CompactPicker } from 'react-color';
import { getGameByID, makeMove } from "../../services/game_service";
import Modal from '@mui/material/Modal';
import { Link } from "react-router-dom";
import { Box, Typography } from "@mui/material";
import { socket } from '../../services/socket';

interface State {
    id: number;
    gameType: GameType;
    board: number[][];
    winner: boolean; // 0 = no winner, 1 = player 1, 2 = player 2
    playerTurn: number; // 1 = player 1, 2 = player 2
    myTurn: boolean;
    player1Score: number;
    player2Score: number;
    possibleMoves: Number[][];
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
    constructor(props: Props) {
        super(props);
        const { gameType, id } = getGameInfoFromURL();
        this.state = {
            id: id,
            gameType: gameType,
            board: [],
            winner: false,
            playerTurn: 1,
            myTurn: true,
            player1Score: 2,
            player2Score: 2,
            possibleMoves: [],
            // ui stuff
            player1Color: "#000000",
            player2Color: "#FFF",
            boardColor1: "#769656",
            boardColor2: "#eeeed2",
            showSettings: false,
            rotateIcon: false
        }
    }

    componentDidMount(): void {
        // get game info
        this.getGameInfo();

        if (this.state.gameType === GameType.Online) {
            socket.on('connect', () => {
                console.log('connected')
            })
            socket.on('disconnect', () => {
                console.log('disconnected')
            })
            socket.on('makeMove', (data) => {
                this.getGameInfo();
            })

            socket.connect();
        }
    }

    componentWillUnmount(): void {
        if (this.state.gameType === GameType.Online) {
            socket.disconnect();
            socket.off('connect');
            socket.off('disconnect');
            socket.off('makeMove');
        }
    }

    async getGameInfo() {
        const game = await getGameByID(this.state.id);
        this.setState({
            board: game.board,
            player1Score: game.player1Score,
            player2Score: game.player2Score,
            possibleMoves: game.possibleMoves,
            winner: game.winner,
            playerTurn: game.currentPlayer,
            myTurn: this.state.gameType === GameType.Online ? 
                (game.player1.userID === this.props.token && game.currentPlayer === 1 
                    || game.player2.userID === this.props.token && game.currentPlayer === 2) 
                : game.currentPlayer === 1
        })
        console.log(game, this.state)
    }

    async makeMove(row: number, col: number) {
        if (this.state.gameType === GameType.Online) {
            socket.emit('makeMove', {
                gameID: this.state.id,
                move: { x: row, y: col },
                gameType: this.state.gameType
            });
            this.getGameInfo();
        } else {
            const res = await makeMove({
                gameID: this.state.id, 
                move: { x: row, y: col },
                gameType: this.state.gameType
            });
            if (res) {
                this.getGameInfo();
            }
        }
    }

    render(): React.ReactNode {
        return (
            <div className="App">
                <small>Type: {this.state.gameType.toLocaleUpperCase()}</small>
                <div className="board">
                    {
                        this.state.winner &&
                            <p style={{
                                fontSize: '2em',
                                color: 'white'
                            }}>
                                { 
                                    this.state.player1Score === this.state.player2Score ? 
                                    "Tie!" :
                                    this.state.player1Score > this.state.player2Score ?
                                    "Player 1 Wins!" : "Player 2 Wins!" 
                                }
                            </p>
                    }
                    <p style={{
                        fontSize: '2em',
                        color: 'white'
                    }}>
                        { this.state.player1Score } : { this.state.player2Score } <br/>
                        - Player { this.state.playerTurn } Turn -
                    </p>
                    <table>
                        <tbody>
                        {
                            this.state.board.map((row, i) => {
                                return (
                                    <tr key={i}>
                                        {
                                            row.map((col, j) => {
                                                return (
                                                    <td key={j} 
                                                        style={{
                                                            backgroundColor: (i + j) % 2 === 0 ? this.state.boardColor1 : this.state.boardColor2,
                                                            borderColor: (i + j) % 2 === 0 ? this.state.boardColor2 : this.state.boardColor1,
                                                        }}
                                                    >
                                                        {
                                                            col === 0 && this.state.myTurn ? 
                                                            this.state.possibleMoves.some(move => move[0] === j && move[1] === i) ? 
                                                                    this.state.playerTurn !== 1 ? 
                                                                    <div 
                                                                        className="player" 
                                                                        style={{
                                                                            backgroundColor: this.state.player1Color,
                                                                            opacity: 0.3
                                                                        }}
                                                                        onClick={() => this.makeMove(j, i)}
                                                                    /> 
                                                                    : 
                                                                    <div 
                                                                        className="player" 
                                                                        style={{
                                                                            backgroundColor: this.state.player2Color,
                                                                            opacity: 0.3
                                                                        }}
                                                                        onClick={() => this.makeMove(j, i)}
                                                                    />
                                                                : <div className="empty"/>
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
                    { this.renderWinnerModal() }
                    { this.renderSettings() }
                </div>
            </div>
        );
    }

    renderWinnerModal(): React.ReactNode {
        const style = {
            position: 'absolute' as 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: 400,
            bgcolor: '#282c34',
            color: 'white',
            border: '2px solid #000',
            font: '',
            boxShadow: 24,
            p: 4,
        };
        return (
            this.state.winner &&
            <div>
                <Modal
                    open={this.state.winner}
                    onClose={() => {

                    }}
                    aria-labelledby="modal-modal-title"
                    aria-describedby="modal-modal-description"
                >
                    <Box sx={style}>
                        <Typography id="modal-modal-title" variant="h6" component="h2">
                            { 
                                this.state.player1Score == this.state.player2Score ? 
                                "Tie!" :
                                this.state.player1Score > this.state.player2Score ?
                                "Player 1 Wins!" : "Player 2 Wins!" 
                            }
                        </Typography>
                        <Link to={'/play/' + (this.state.gameType)}>
                            Back to lobby
                        </Link>
                    </Box>
                </Modal>
            </div>
        )
    }

    renderSettings(): React.ReactNode {
        return (
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
        )
    }
}

export enum GameType {
    Online = "online",
    AI = "ai",
    Local = "local"
}

function getGameInfoFromURL(): { gameType: GameType, id: number } {
    const url = window.location.pathname;
    const urlSplit = url.split('/');
    const gameType = urlSplit[2];
    const gameId = urlSplit[3];
    return {gameType: gameType as GameType, id: parseInt(gameId)};
}
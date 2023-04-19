import { Link } from "react-router-dom";
import "../App.scss"
import { useToken } from "../hooks/use_token";
import { getLeaderboard, getUserByID } from "../services/user_service";
import { useCallback, useEffect, useState } from "react";

// Leaderboard component, shows the leaderboard
export function Leaderboard() {
    const [leaderboard, setLeaderboard] = useState<any[]>([]);

    useEffect(() => {
        const fetchData = async () => {
            const res = await getLeaderboard();
            setLeaderboard(res);
        }

        fetchData();
    }, []);

    return (
        <div className="App">
            <header className="App-header" style={{padding: '40px 0'}}>
                <p>Leaderboard</p>
            </header>
            <div className="App-body">
                <table style={{height: 'fit-content'}}>
                    <thead style={{color: 'black'}}>
                        <tr>
                            <th style={{padding: '10px'}}>Username</th>
                            <th style={{padding: '10px'}}>Elo</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            leaderboard.map((elo, index) => (
                                <tr key={index}>
                                    <td>{elo.username ? elo.username : ('Guest' + elo.userID)}</td>
                                    <td>{elo.elo}</td>
                                </tr>
                            ))
                        }
                    </tbody>
                </table>
            </div>
        </div>
    );
}
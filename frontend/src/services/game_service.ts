// This file contains all the functions that are used to communicate with the backend, related to games

// getGames is used to get all games
export async function getGames() {
    return fetch(process.env.REACT_APP_API_URL!, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json())
}

// getGamesByType is used to get all games of a certain type
export async function getGamesByType(type: string) {
    return fetch(process.env.REACT_APP_API_URL! + type, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json())
}

// getGamesByTypeByUserID is used to get all games of a certain type that a user is involved in
export async function getGamesByTypeByUserID(gameType: string, id: string) {
    return fetch(process.env.REACT_APP_API_URL! + '/games/' + gameType + '/' + id, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json())
}

// createGame is used to create a new game
export async function createGame(body: {
    gameType: string,
    player1ID: number,
    player2ID: number,
    size: number,
    difficulty: number
}) {
    return fetch(process.env.REACT_APP_API_URL! + '/games', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    }).then(data => data.json())
}

// getGameByID is used to get a game by its ID
export async function getGameByID(id: number) {
    return fetch(process.env.REACT_APP_API_URL! + '/games/' + id, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json())
}

// makeMove is used to make a move in a game
export async function makeMove(body: {
    gameID: number,
    gameType: string,
    move: { x: number, y: number },
}) {
    return fetch(process.env.REACT_APP_API_URL! + '/games', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    }).then(data => data.json())
}
export async function getGames() {
    return fetch(process.env.REACT_APP_API_URL!, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json())
}

export async function getGamesByType(type: string) {
    return fetch(process.env.REACT_APP_API_URL! + type, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json())
}

export async function getAIGamesByUserID(id: string) {
    return fetch(process.env.REACT_APP_API_URL! + '/games/ai/' + id, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json())
}

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

export async function getGameByID(id: number) {
    return fetch(process.env.REACT_APP_API_URL! + '/games/' + id, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json())
}

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
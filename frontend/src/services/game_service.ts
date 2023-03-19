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
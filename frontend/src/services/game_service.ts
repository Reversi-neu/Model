export async function getGames() {
    return fetch(process.env.API_URL!, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json'
        }
    }).then(data => data.json())
}

export async function getGamesByType(type: string) {
    return fetch(process.env.API_URL! + type, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json'
        }
    }).then(data => data.json())
}
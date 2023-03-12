export async function getGames() {
    return fetch(process.env.API_URL!, {
        method: 'GET',
        headers: {
        'Content-Type': 'application/json'
        }
    }).then(data => data.json())
}
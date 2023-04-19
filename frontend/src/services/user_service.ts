// This file contains all the functions that interact with the backend API, related to users

// getUserByID is used to get a user by its ID
export async function getUserByID(userID: number) {
    return fetch(process.env.REACT_APP_API_URL! + '/user/' + userID, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json())
}

// loginUser is used to login a user
export async function loginUser(credentials: {username: string, password: string}) {
    return fetch(process.env.REACT_APP_API_URL!+'/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(data => data.json());
}

// signupUser is used to signup a user
export async function signupUser(credentials: {username: string, password: string}) {
    return fetch(process.env.REACT_APP_API_URL!+'/signup', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(data => data.json());
}

// signupGuest is used to signup a guest
export async function signupGuest() {
    return fetch(process.env.REACT_APP_API_URL!+'/guest', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json());
}

// getLeaderboard is used to get the leaderboard
export async function getLeaderboard() {
    return fetch(process.env.REACT_APP_API_URL!+'/leaderboard', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json());
}
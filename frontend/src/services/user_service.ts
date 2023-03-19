import { useToken } from "../hooks/use_token";

export async function loginUser(credentials: {username: string, password: string}) {
    return fetch(process.env.REACT_APP_API_URL!+'/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(data => data.json());
}

export async function signupUser(credentials: {username: string, password: string}) {
    return fetch(process.env.REACT_APP_API_URL!+'/signup', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(data => data.json());
}

export async function signupGuest() {
    return fetch(process.env.REACT_APP_API_URL!+'/guest', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(data => data.json());
}
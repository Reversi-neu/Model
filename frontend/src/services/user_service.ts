import { useToken } from "../hooks/use_token";

export async function loginUser(credentials: {username: string, password: string}) {
    return fetch(process.env.REACT_APP_API_URL!, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(data => data.json());
    // return 'test';
}
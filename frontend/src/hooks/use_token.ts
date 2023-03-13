import { useState } from 'react';

export function useToken() {
  const getToken = () => {
    const tokenString = sessionStorage.getItem('token')!;
    const userToken = JSON.parse(tokenString);
    // return userToken?.token
    return userToken;
  };

  const [token, setToken] = useState(getToken());

  const saveToken = (userToken?: string) => {
    sessionStorage.setItem('token', JSON.stringify(userToken || null));
    setToken(userToken);
  };

  return {
    setToken: saveToken,
    token
  }
}
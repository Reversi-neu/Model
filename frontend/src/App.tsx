import './App.scss';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Title } from './components/title';
import { Board } from './components/board/board';
import { Login } from './components/login';
import { useToken } from './hooks/use_token';
import { Settings } from './components/settings';
import { Sidebar } from './components/sidebar/sidebar';
import { LocalMenu } from './components/local_menu';
import { OnlineMenu } from './components/online_menu';
import { LobbyManager } from './components/lobbies_manager';
import { Leaderboard } from './components/leaderboard';

// App is the main component of the application
function App() {
  const { token, setToken } = useToken();
  
  return (
    <BrowserRouter>
      <Sidebar/>
      <Routes>
        <Route path="*" element={
          <Title/>
        }/>
        <Route path="settings" element={
          <Settings/>
        }/>
        <Route path="login" element={
          <Login token={token} setToken={setToken} />
        }/>
        <Route path="online" element={
          <OnlineMenu/>
        }/>
        <Route path="local" element={
          <LocalMenu/>
        }/>
        <Route path="play/:gameType" element={ 
          <LobbyManager/>
        }/>
        <Route path="play/:gameType/:id" element={
          <Board token={token}/>
        }/>
        <Route path="leaderboard" element={
          <Leaderboard />
        }/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;

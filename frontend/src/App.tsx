import './App.scss';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Title } from './components/title';
import { Board } from './components/board/board';
import { Login } from './components/login';
import { useToken } from './hooks/useToken';
import { Settings } from './components/settings';
import { Icons } from './components/icons';
import { LocalMenu } from './components/localMenu';
import { OnlineMenu } from './components/onlineMenu';

function App() {
  const { token, setToken } = useToken();
  
  return (
    <BrowserRouter>
      <Icons/>
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
          // <Board token={token} gameType={GameType.Online}/>
        }/>
        <Route path="local" element={
          <LocalMenu/>
          // <Board token={token} gameType={GameType.Local}/>
        }/>
        <Route path="play/:gameType" element={
          <Board token={token}/>
        }/>
        {/* <Route path="ai" element={
          <Board token={token} gameType={GameType.AI}/>
        }/> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;

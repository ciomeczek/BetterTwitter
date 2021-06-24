import React, { useState } from 'react';
import Login from './Components/LoginSystem/Login.js';
import Signup from './Components/LoginSystem/Signup.js';
import Home from './Components/Home/Home'
import Posts from './Components/Posts/Posts'
import Friends from './Components/Friends/Friends'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

function App() {
  const [islogged, setIslogged] = useState(false);
    const loginForm = (
      <>
        <div onClick={Login}>Zaloguj</div>
        <div onClick={Signup}>Zarejestruj</div>
      </>
  )
    const viewusername = localStorage.getItem('username');
    const logoutForm = (
      <>
        <button onClick={()=>localStorage.removeItem('username'), ()=>setIslogged(!islogged)}>Wyloguj</button>
        <h3>Witaj {viewusername}</h3>
      </>
    );
    return (
        <>
            <h2 className="Logo">Bwitter</h2>
            <Router>
              <div>
                <nav>
                  <ul>
                    <li>
                      <Link to="/">Główna</Link>
                    </li>
                    <li>
                      <Link to="/posty">Posty</Link>
                    </li>
                    <li>
                      <Link to="/znajomi">Znajomi</Link>
                    </li>
                  </ul>
                </nav>
                <div>{islogged ? logoutForm : loginForm}</div>
                <Switch>
                  <Route path="/posty">
                    <Posts />
                  </Route>
                  <Route path="/znajomi">
                    <Friends />
                  </Route>
                  <Route path="/">
                    <Home />
                  </Route>
                </Switch>
              </div>
            </Router>
        </>
    )
}

export default App;

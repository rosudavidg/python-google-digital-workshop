import './App.css';
import { BrowserRouter, Switch, Route, Redirect } from "react-router-dom";
import Header from "./Header"
import HomePage from "./HomePage"
import Home from "./Home"
import Login from "./Login"
import Register from "./Register"
import { useState } from "react"
import 'bootstrap/dist/css/bootstrap.css';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem("token") != null);

  return (
    <div className="app">
      <BrowserRouter>
        <Header />
        <Switch>
          <Route
            exact
            path="/"
            render={() => {
              if (isLoggedIn) {
                return <Home setIsLoggedIn={setIsLoggedIn} />;
              } else {
                return <HomePage />;
              }
            }}
          />
          <Route
            exact
            path="/register"
            render={() => {
              if (isLoggedIn) {
                return <Home setIsLoggedIn={setIsLoggedIn} />;
              } else {
                return <Register />;
              }
            }}
          />
          <Route
            exact
            path="/login"
            render={() => {
              if (isLoggedIn) {
                return <Home setIsLoggedIn={setIsLoggedIn} />;
              } else {
                return <Login setIsLoggedIn={setIsLoggedIn} />;
              }
            }}
          />
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;

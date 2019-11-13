import React from "react";
import Header from "./Header";
import { MuiThemeProvider, createMuiTheme } from "@material-ui/core/styles";
import "./App.css";
import orange from "@material-ui/core/colors/orange";
import red from "@material-ui/core/colors/red";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from "react-router-dom";
import Serie from "./Serie";
import Login from "./Login";
import Signup from "./Signup";
import Home from "./Home";
import FavoriteSeries from "./FavoriteSeries";

import ky from "ky";

(async () => {
  try {
    const parsed = await ky
      .get(
        "https://api.themoviedb.org/3/movie/550?api_key=84eae13884eb7a9e47fcc760ca08f59"
      )
      .json();

    console.log(parsed);
  } catch (error) {
    const serverMessage = await error.response.text();
    console.log("Server error: " + serverMessage);
  }
  //=> `{data: '🦄'}`
})();

const fakeAuth = {
  isAuthenticated: false,
  authenticate: function() {
    return new Promise(resolve => {
      setTimeout(() => {
        this.isAuthenticated = true;
        resolve(this.isAuthenticated);
      }, 1000);
    });
  },
  signout: function() {
    return new Promise(resolve => {
      setTimeout(() => {
        this.isAuthenticated = false;
        resolve(this.isAuthenticated);
      }, 1000);
    });
  }
};

const PrivateRoute = ({ component: Component, ...rest }) => (
  <Route
    {...rest}
    render={props =>
      fakeAuth.isAuthenticated === true ? (
        <Component {...props} />
      ) : (
        <Redirect to="/login" />
      )
    }
  />
);

const GuestRoute = ({ component: Component, ...rest }) => (
  <Route
    {...rest}
    render={props =>
      fakeAuth.isAuthenticated === false ? (
        <Redirect to="/login" />
      ) : (
        <Component {...props} />
      )
    }
  />
);

const theme = createMuiTheme({
  palette: {
    primary: orange,
    secondary: red
  },
  status: {
    danger: "orange"
  }
});

function App() {
  return (
    <MuiThemeProvider theme={theme}>
      <Router>
        <Header className="App-header"> </Header>
        <div
          style={{
            position: "absolute",
            display: "flex",
            width: "100%",
            height: "100%",
            alignItems: "center",
            zIndex: 2
          }}
        >
          <Switch>
            <PrivateRoute path="/serie/:id" component={Serie}></PrivateRoute>
            <PrivateRoute
              path="/favorites"
              component={FavoriteSeries}
            ></PrivateRoute>
            <Route path="/login" component={Login}></Route>
            <Route path="/signup" component={Signup}></Route>
            <GuestRoute path="/" component={Home}></GuestRoute>
          </Switch>
        </div>
      </Router>
    </MuiThemeProvider>
  );
}

export { App, fakeAuth };

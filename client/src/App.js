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
        <Switch>
          <PrivateRoute path="/serie/:id" component={Serie}></PrivateRoute>
          <Route path="/login" component={Login}></Route>
          <Route path="/signup" component={Signup}></Route>
          <GuestRoute path="/" component={Home}></GuestRoute>
        </Switch>
      </Router>
    </MuiThemeProvider>
  );
}

export { App, fakeAuth };

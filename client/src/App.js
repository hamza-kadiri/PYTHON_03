import orange from "@material-ui/core/colors/orange";
import grey from "@material-ui/core/colors/grey";
import { createMuiTheme, MuiThemeProvider } from "@material-ui/core/styles";
import React from "react";
import { Router, Redirect, Route, Switch } from "react-router-dom";
import "./App.css";
import FavoriteSeries from "./FavoriteSeries";
import Header from "./Header";
import { history } from "./helpers/history";
import Home from "./Home";
import Login from "./Login";
import Serie from "./Serie";
import Signup from "./Signup";

const PrivateRoute = ({ component: Component, ...rest }) => (
  <Route
    {...rest}
    render={props =>
      localStorage.getItem("user") ? (
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
      !localStorage.getItem("user") ? (
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
    secondary: grey,
    text: {
      primary: "#ffffff",
      secondary: "#00000"
    }
  },
  status: {
    danger: "orange"
  },
  overrides: {
    MuiMenu: {
      paper: {
        backgroundColor: "rgba(255, 152, 0, 0.85)",
        color: "white"
      }
    },
    MuiBadge: {
      colorPrimary: {
        backgroundColor: orange[300]
      },
      colorSecondary: {
        backgroundColor: orange[800]
      }
    }
  }
});

function App() {
  return (
    <MuiThemeProvider theme={theme}>
      <Router history={history}>
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

export { App };

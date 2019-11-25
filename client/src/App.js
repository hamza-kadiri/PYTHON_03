import orange from "@material-ui/core/colors/orange";
import grey from "@material-ui/core/colors/grey";
import { createMuiTheme, MuiThemeProvider } from "@material-ui/core/styles";
import React, { useState, useEffect } from "react";
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
    },
    MuiSelect: {
      root: {
        borderBottom: "2px solid white"
      },
      select: {
        color: "white"
      },
      icon: {
        color: "white"
      }
    },
    MuiDivider: {
      root: {
        marginLeft: "5px",
        marginRight: "5px",
        backgroundColor: "rgb(255,255,255,0.08)"
      }
    }
  }
});

function App() {
  const [scrollY, setScrollY] = useState(0);

  function logit() {
    setScrollY(window.pageYOffset);
  }

  useEffect(() => {
    function watchScroll() {
      window.addEventListener("scroll", logit);
    }
    watchScroll();
    // Remove listener (like componentWillUnmount)
    return () => {
      window.removeEventListener("scroll", logit);
    };
  });
  return (
    <MuiThemeProvider theme={theme}>
      <Router history={history}>
        <Header scrollY={scrollY} className="App-header"></Header>
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

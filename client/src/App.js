import React from "react";
import Header from "./Header";
import { MuiThemeProvider, createMuiTheme } from "@material-ui/core/styles";
import "./App.css";
import orange from "@material-ui/core/colors/orange";
import red from "@material-ui/core/colors/red";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Serie from "./Serie";

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
          <Route path="/serie/:id" component={Serie}></Route>
          <Route path="/"></Route>
        </Switch>
      </Router>
    </MuiThemeProvider>
  );
}

export default App;

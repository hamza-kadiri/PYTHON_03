import React from "react";
import logo from "./logo.svg";
import Header from "./Header";
import { MuiThemeProvider, createMuiTheme } from "@material-ui/core/styles";
import "./App.css";
import orange from "@material-ui/core/colors/orange";
import red from "@material-ui/core/colors/red";

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
      <Header className="App-header"> </Header>
    </MuiThemeProvider>
  );
}

export default App;

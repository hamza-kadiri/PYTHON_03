import React, { useEffect, useState } from "react";
import Button from "@material-ui/core/Button";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardHeader from "@material-ui/core/CardHeader";
import Input from "@material-ui/core/Input";
import InputLabel from "@material-ui/core/InputLabel";
import InputAdornment from "@material-ui/core/InputAdornment";
import FormControl from "@material-ui/core/FormControl";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import AccountCircle from "@material-ui/icons/AccountCircle";
import Lock from "@material-ui/icons/Lock";
import Typography from "@material-ui/core/Typography";
import ky from "ky";
import { Link, Redirect, useHistory } from "react-router-dom";
import CircularProgress from "@material-ui/core/CircularProgress";
import { fakeAuth } from "./App";
import { userLogin } from "./redux/actions";
import { connect, useDispatch } from "react-redux";

const useStyles = makeStyles(theme => ({
  margin: {
    margin: theme.spacing(1)
  },
  link: {
    color: theme.palette.primary.main
  }
}));

const Login = ({ match }) => {
  let history = useHistory();
  const classes = useStyles();
  const [isLoading, setisLoading] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const dispatch = useDispatch();
  const handleLogin = async () => {
    setisLoading(true);
    await dispatch(userLogin({ username, password }));
    setisLoading(false);
  };
  return (
    <React.Fragment>
      <div
        style={{
          opacity: 0.4,
          background: `linear-gradient(
                to top,
                rgba(0,0,0, 20),
                rgba(0,0,0, 0)
              ), url('/background.jpg')`,
          backgroundSize: "cover",
          position: "absolute",
          display: "flex",
          width: "100%",
          height: "100%",
          alignItems: "center",
          justifyContent: "center",
          zIndex: -1
        }}
      ></div>
      <div
        style={{
          position: "absolute",
          opacity: 0.9,
          display: "flex",
          width: "100%",
          height: "100%",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 2
        }}
      >
        <Card style={{ background: "rgba(0,0,0,0.6)" }}>
          <CardContent style={{ color: "white" }}>
            <Typography component="h5" variant="h5">
              Log In
            </Typography>
            <Grid container direction="column" alignItems="center" spacing={1}>
              <Grid item></Grid>
              <Grid item>
                <FormControl
                  style={{ color: "white" }}
                  className={classes.margin}
                >
                  <InputLabel
                    style={{ color: "white", fontSize: "20px" }}
                    htmlFor="input-login"
                  >
                    Login
                  </InputLabel>
                  <Input
                    style={{ color: "white", fontSize: "20px" }}
                    id="input-login"
                    placehoder="Login"
                    onChange={e => setUsername(e.target.value)}
                    startAdornment={
                      <InputAdornment position="start">
                        <AccountCircle />
                      </InputAdornment>
                    }
                  />
                </FormControl>
              </Grid>
              <Grid>
                <FormControl className={classes.margin}>
                  <InputLabel
                    style={{ color: "white", fontSize: "20px" }}
                    htmlFor="input-password"
                  >
                    Password
                  </InputLabel>
                  <Input
                    style={{ color: "white", fontSize: "20px" }}
                    id="input-password"
                    type="password"
                    placehoder="Password"
                    onChange={e => setPassword(e.target.value)}
                    startAdornment={
                      <InputAdornment position="start">
                        <Lock />
                      </InputAdornment>
                    }
                  />
                </FormControl>
              </Grid>
              <Grid item style={{ width: "40%" }}>
                <Button
                  color="primary"
                  variant="outlined"
                  onClick={handleLogin}
                  style={{ width: "100%", height: "35px" }}
                >
                  {isLoading ? (
                    <CircularProgress size={20} color="primary" />
                  ) : (
                    "Log In"
                  )}
                </Button>
              </Grid>
              <Grid item style={{ width: "100%" }}>
                <Typography variant="caption">
                  Don't have an account ?{" "}
                  <Link className={classes.link} to="/signup">
                    Sign up
                  </Link>
                  {" first."}
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </div>
    </React.Fragment>
  );
};

export default Login;

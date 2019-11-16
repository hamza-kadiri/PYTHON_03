import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CircularProgress from "@material-ui/core/CircularProgress";
import FormControl from "@material-ui/core/FormControl";
import Grid from "@material-ui/core/Grid";
import Input from "@material-ui/core/Input";
import InputAdornment from "@material-ui/core/InputAdornment";
import InputLabel from "@material-ui/core/InputLabel";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import AccountCircle from "@material-ui/icons/AccountCircle";
import Lock from "@material-ui/icons/Lock";
import Mail from "@material-ui/icons/Mail";
import React, { useState } from "react";
import { connect, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import { userSignup } from "./actions/signup.actions";

const useStyles = makeStyles(theme => ({
  margin: {
    margin: theme.spacing(1)
  },
  link: {
    color: theme.palette.primary.main
  }
}));

const Signup = ({ match, isLoading }) => {
  const classes = useStyles();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const dispatch = useDispatch();
  const handleSignup = async () => {
    await dispatch(userSignup({ username, password, email }));
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
        <Card
          onKeyPress={e => e.key === "Enter" && handleSignup()}
          style={{ background: "rgba(0,0,0,0.6)" }}
        >
          <CardContent style={{ color: "white" }}>
            <Typography component="h5" variant="h5">
              Sign up
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
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                    startAdornment={
                      <InputAdornment position="start">
                        <AccountCircle />
                      </InputAdornment>
                    }
                  />
                </FormControl>
              </Grid>
              <Grid item>
                <FormControl
                  style={{ color: "white" }}
                  className={classes.margin}
                >
                  <InputLabel
                    style={{ color: "white", fontSize: "20px" }}
                    htmlFor="input-email"
                  >
                    Email
                  </InputLabel>
                  <Input
                    style={{ color: "white", fontSize: "20px" }}
                    id="input-email"
                    placehoder="Email"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    startAdornment={
                      <InputAdornment position="start">
                        <Mail />
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
                    value={password}
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
                  onClick={handleSignup}
                  style={{ width: "100%", height: "35px" }}
                >
                  {isLoading ? (
                    <CircularProgress size={20} color="primary" />
                  ) : (
                    "Sign up"
                  )}
                </Button>
              </Grid>
              <Grid item style={{ width: "100%" }}>
                <Typography variant="caption">
                  Already have an account ?{" "}
                  <Link className={classes.link} to="/login">
                    Log In
                  </Link>
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </div>
    </React.Fragment>
  );
};

const mapStateToProps = ({ user }) => {
  return {
    isLoading: user.isFetching
  };
};
export default connect(mapStateToProps)(Signup);

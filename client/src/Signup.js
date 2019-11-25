import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CircularProgress from "@material-ui/core/CircularProgress";
import FormControl from "@material-ui/core/FormControl";
import FormHelperText from "@material-ui/core/FormHelperText";
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
import { userSignup, actions } from "./actions/signup.actions";
import MessageSnackbar from "./MessageSnackbar";

const useStyles = makeStyles(theme => ({
  margin: {
    margin: theme.spacing(1)
  },
  link: {
    color: theme.palette.primary.main
  },
  input: { color: "white", fontSize: "20px" }
}));

const Signup = ({ match, isLoading, error }) => {
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
          flexDirection: "column",
          zIndex: 2
        }}
      >
        {error && error.error_message && (
          <MessageSnackbar
            variant="error"
            message={error.error_message}
            onClose={() => dispatch({ type: actions.USER_SIGNUP_RESET_STATE })}
          ></MessageSnackbar>
        )}
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
                  error={
                    error &&
                    error.invalid_fields &&
                    "username" in error.invalid_fields
                  }
                >
                  <InputLabel
                    error={
                      error &&
                      error.invalid_fields &&
                      "username" in error.invalid_fields
                    }
                    className={classes.input}
                    htmlFor="input-login"
                  >
                    Login
                  </InputLabel>
                  <Input
                    className={classes.input}
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
                  {error &&
                    error.invalid_fields &&
                    "username" in error.invalid_fields && (
                      <FormHelperText>
                        {error &&
                          error.invalid_fields &&
                          error.invalid_fields.username}
                      </FormHelperText>
                    )}
                </FormControl>
              </Grid>
              <Grid item>
                <FormControl
                  style={{ color: "white" }}
                  className={classes.margin}
                  error={
                    error &&
                    error.invalid_fields &&
                    "email" in error.invalid_fields
                  }
                >
                  <InputLabel
                    className={classes.input}
                    error={
                      error &&
                      error.invalid_fields &&
                      "email" in error.invalid_fields
                    }
                    htmlFor="input-email"
                  >
                    Email
                  </InputLabel>
                  <Input
                    className={classes.input}
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
                  {error &&
                    error.invalid_fields &&
                    "email" in error.invalid_fields && (
                      <FormHelperText>
                        {error &&
                          error.invalid_fields &&
                          error.invalid_fields.email}
                      </FormHelperText>
                    )}
                </FormControl>
              </Grid>
              <Grid>
                <FormControl
                  error={
                    error &&
                    error.invalid_fields &&
                    "password" in error.invalid_fields
                  }
                  className={classes.margin}
                >
                  <InputLabel
                    className={classes.input}
                    htmlFor="input-password"
                    error={
                      error &&
                      error.invalid_fields &&
                      "password" in error.invalid_fields
                    }
                  >
                    Password
                  </InputLabel>
                  <Input
                    className={classes.input}
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
                  {error &&
                    error.invalid_fields &&
                    "password" in error.invalid_fields && (
                      <FormHelperText>
                        {error &&
                          error.invalid_fields &&
                          error.invalid_fields.password}
                      </FormHelperText>
                    )}
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

const mapStateToProps = ({ signup }) => {
  return {
    isLoading: signup.isFetching,
    error: signup.error
  };
};
export default connect(mapStateToProps)(Signup);

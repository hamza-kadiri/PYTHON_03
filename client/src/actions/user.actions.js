import clientWeb from "../helpers/clientWeb";
import { history } from "../helpers/history";

export const actions = {
  REQUEST_USER_SIGNUP: "REQUEST_USER_SIGNUP",
  USER_SIGNUP_ERROR: "USER_SIGNUP_ERROR",
  REQUEST_USER_TOKEN: "REQUEST_USER_TOKEN",
  RECEIVE_USER_TOKEN: "RECEIVE_USER_TOKEN",
  USER_TOKEN_ERROR: "USER_TOKEN_ERROR",
  USER_LOGOUT: "USER_LOGOUT"
};

const requestUserToken = user => {
  return {
    type: actions.REQUEST_USER_TOKEN,
    user
  };
};

const receiveUserToken = response => {
  let token = response.token;
  let user = { ...response.user, token };
  localStorage.setItem("user", JSON.stringify(user));
  return {
    type: actions.RECEIVE_USER_TOKEN,
    response,
    receivedAt: Date.now()
  };
};

export const userSignup = user => {
  return async dispatch => {
    try {
      const response = await clientWeb.post(`users`, { json: user });
      response.ok && dispatch(userLogin(user));
    } catch (error) {
      const error_response = await error.response.json();
      dispatch({ type: actions.USER_SIGNUP_ERROR, error: error_response });
    }
  };
};

export const userLogin = user => {
  return async dispatch => {
    try {
      dispatch(requestUserToken(user));
      const response = await clientWeb.post(`token`, {
        json: user
      });
      const json = await response.json();
      dispatch(receiveUserToken(json));
      history.push("/");
    } catch (error) {
      const error_response = await error.response.json();
      dispatch({ type: actions.USER_TOKEN_ERROR, error: error_response });
    }
  };
};

export const userLogout = () => {
  localStorage.removeItem("user");
  return {
    type: actions.USER_LOGOUT
  };
};

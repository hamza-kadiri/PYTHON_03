import clientWeb from "../helpers/clientWeb";
import { history } from "../helpers/history";
import { handleError } from "./common.actions";

export const actions = {
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
export const userLogin = user => {
  return async dispatch => {
    try {
      await dispatch(requestUserToken(user));
      const response = await clientWeb.post(`token`, {
        json: user
      });
      const json = await response.json();
      await dispatch(receiveUserToken(json));
      history.push("/");
    } catch (error) {
      dispatch(handleError(error, actions.USER_TOKEN_ERROR));
    }
  };
};

export const userLogout = () => {
  localStorage.removeItem("user");
  history.push("/");
  return {
    type: actions.USER_LOGOUT
  };
};

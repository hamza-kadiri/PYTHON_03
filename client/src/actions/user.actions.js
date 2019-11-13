import ky from "ky";

export const actions = {
  REQUEST_USER_SIGNUP: "REQUEST_USER_SIGNUP",
  USER_SIGNUP_ERROR: "USER_SIGNUP_ERROR",
  REQUEST_USER_TOKEN: "REQUEST_USER_TOKEN",
  RECEIVE_USER_TOKEN: "RECEIVE_USER_TOKEN",
  USER_TOKEN_ERROR: "USER_TOKEN_ERROR"
};

const requestUserToken = user => {
  return {
    type: actions.REQUEST_USER_TOKEN,
    user
  };
};

const receiveUserToken = response => {
  return {
    type: actions.RECEIVE_USER_TOKEN,
    response,
    receivedAt: Date.now()
  };
};

export const userSignup = user => {
  return async dispatch => {
    try {
      const response = await ky.post(`//localhost:8001/users`, { json: user });
      const json = await response.json();
      dispatch(userLogin(user));
    } catch (error) {
      console.log(error.response);
      const error_response = await error.response.json();
      dispatch({ type: actions.USER_SIGNUP_ERROR, error: error_response });
    }
  };
};

export const userLogin = user => {
  return async dispatch => {
    try {
      dispatch(requestUserToken(user));
      const response = await ky.post(`//localhost:8001/token`, { json: user });
      const json = await response.json();
      dispatch(receiveUserToken(json));
    } catch (error) {
      console.log(error.response);
      const error_response = await error.response.json();
      dispatch({ type: actions.USER_TOKEN_ERROR, error: error_response });
    }
  };
};

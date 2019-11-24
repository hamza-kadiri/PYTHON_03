import clientWeb from "../helpers/clientWeb";
import { userLogin } from "./auth.actions";
import { handleError } from "./common.actions";

export const actions = {
  REQUEST_USER_SIGNUP: "REQUEST_USER_SIGNUP",
  USER_SIGNUP_ERROR: "USER_SIGNUP_ERROR",
  USER_SIGNUP_SUCCESS: "USER_SIGNUP_SUCCESS",
  USER_SIGNUP_RESET_STATE: "USER_SIGNUP_RESET_STATE"
};

export const userSignup = user => {
  return async dispatch => {
    try {
      dispatch({
        type: actions.REQUEST_USER_SIGNUP,
        user: { username: user.username, email: user.email }
      });
      const response = await clientWeb.post(`users`, { json: user });
      response.ok &&
        dispatch({
          type: actions.USER_SIGNUP_SUCCESS,
          user: { username: user.username, email: user.email }
        }) &&
        dispatch(userLogin(user));
    } catch (error) {
      dispatch(handleError(error, actions.USER_SIGNUP_ERROR));
    }
  };
};

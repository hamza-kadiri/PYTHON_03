import { userLogout } from "./auth.actions";

export const handleError = (error, errorAction) => {
  return async dispatch => {
    const errorResponse = await error.response;
    const errorMessage = await errorResponse.json();
    const status = errorResponse.status;
    if (status == 401) {
      dispatch(userLogout());
    }
    dispatch({
      type: errorAction,
      error: { ...errorMessage }
    });
  };
};

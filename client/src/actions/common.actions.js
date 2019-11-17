import { userLogout } from "./auth.actions";

export const handleError = (error, errorAction) => {
  return async dispatch => {
    try {
      const errorResponse = await error.response;
      const status = errorResponse.status;
      if (status === 401) {
        await dispatch(userLogout());
      }
      const errorMessage = await errorResponse.json();
      dispatch({
        type: errorAction,
        error: { ...errorMessage }
      });
    } catch (err) {
      console.error(error);
      console.error(err);
    }
  };
};

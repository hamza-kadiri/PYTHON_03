import { actions } from "../actions/user.actions";

export function user(
  state = {
    user: {},
    token: ""
  },
  action
) {
  switch (action.type) {
    case actions.USER_SIGNUP_ERROR:
      return { ...state, isFetching: false, error: action.error };
    case actions.REQUEST_USER_TOKEN:
      return { ...state, isFetching: true };
    case actions.RECEIVE_USER_TOKEN:
      return {
        ...state,
        isFetching: false,
        token: action.response.token,
        user: action.response.user,
        lastUpdated: action.receivedAt
      };
    case actions.USER_TOKEN_ERROR:
      return { ...state, isFetching: false, error: action.error };
    default:
      return state;
  }
}

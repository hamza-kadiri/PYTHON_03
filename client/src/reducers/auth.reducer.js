import { actions } from "../actions/auth.actions";

const initialState = {
  user: {},
  token: "",
  isFetching: false
};
export function user(state = initialState, action) {
  switch (action.type) {
    case actions.REQUEST_USER_TOKEN:
      return { ...state, isFetching: true };
    case actions.RECEIVE_USER_TOKEN:
      return {
        ...initialState,
        isFetching: false,
        token: action.response.token,
        user: action.response.user,
        lastUpdated: action.receivedAt
      };
    case actions.USER_TOKEN_ERROR:
      return { ...initialState, error: action.error };
    case actions.USER_LOGOUT:
      return initialState;
    default:
      return state;
  }
}

import { actions } from "../actions/signup.actions";

const initialState = {
  user: {},
  isFetching: false
};
export function signup(state = initialState, action) {
  switch (action.type) {
    case actions.REQUEST_USER_SIGNUP:
      return { ...state, isFetching: true, user: action.user };
    case actions.USER_SIGNUP_SUCCESS:
      return { ...initialState, isFetching: false, user: action.user };
    case actions.USER_SIGNUP_ERROR:
      return { ...initialState, error: action.error };
    case actions.USER_SIGNUP_RESET_STATE:
      return initialState;
    default:
      return state;
  }
}

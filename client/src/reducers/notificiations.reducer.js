import { actions } from "../actions/notifications.actions";

const initialState = {
  notifications: []
};
export function notifications(state = initialState, action) {
  switch (action.type) {
    case actions.REQUEST_GET_NOTIFICATIONS:
      return { ...state, isFetching: true };
    case actions.SUCCESS_GET_NOTIFICATIONS:
      return {
        ...initialState,
        isFetching: false,
        notifications: action.notifications
      };
    case actions.ERROR_GET_NOTIFICATIONS:
      return { ...initialState, error: action.error };
    default:
      return state;
  }
}

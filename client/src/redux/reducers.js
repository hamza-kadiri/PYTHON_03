import { combineReducers } from "redux";
import { actions } from "./actions";

function suggestedSeries(
  state = {
    isFetching: false,
    suggestions: []
  },
  action
) {
  switch (action.type) {
    case actions.REQUEST_SUGGESTED_SERIES:
      return { ...state, isFetching: true };
    case actions.RECEIVE_SUGGESTED_SERIES:
      return {
        ...state,
        isFetching: false,
        query: action.query,
        suggestions: action.series,
        lastUpdated: action.receivedAt
      };
    default:
      return state;
  }
}

function selectedSerie(
  state = {
    isFetching: false,
    serie: { name: "" }
  },
  action
) {
  switch (action.type) {
    case actions.REQUEST_SERIE:
      return { ...state, isFetching: true };
    case actions.RECEIVE_SERIE:
      return {
        ...state,
        isFetching: false,
        serie: action.serie,
        lastUpdated: action.receivedAt
      };
    case actions.RESET_SERIE:
      return {
        isFetching: false,
        serie: { name: "" }
      };
    default:
      return state;
  }
}

function user(
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

const rootReducer = combineReducers({
  suggestedSeries,
  selectedSerie,
  user
});

export default rootReducer;

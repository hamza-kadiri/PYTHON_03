import { combineReducers } from "redux";
import {
  REQUEST_SUGGESTED_SERIES,
  RECEIVE_SUGGESTED_SERIES,
  REQUEST_SERIE,
  RECEIVE_SERIE,
  RESET_SERIE
} from "./actions";

function suggestedSeries(
  state = {
    isFetching: false,
    suggestions: []
  },
  action
) {
  switch (action.type) {
    case REQUEST_SUGGESTED_SERIES:
      return { ...state, isFetching: true };
    case RECEIVE_SUGGESTED_SERIES:
      return {
        ...state,
        isFetching: false,
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
    case REQUEST_SERIE:
      return { ...state, isFetching: true };
    case RECEIVE_SERIE:
      return {
        ...state,
        isFetching: false,
        serie: action.serie,
        lastUpdated: action.receivedAt
      };
    case RESET_SERIE:
      return {
        isFetching: false,
        serie: { name: "" }
      };
    default:
      return state;
  }
}

const rootReducer = combineReducers({
  suggestedSeries,
  selectedSerie
});

export default rootReducer;

import { actions } from "../actions/series.actions";

export function suggestedSeries(
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

export function selectedSerie(
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

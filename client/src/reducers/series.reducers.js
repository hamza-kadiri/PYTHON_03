import { actions } from "../actions/series.actions";

const suggestedSeriesInitialState = {
  isFetching: false,
  suggestions: [],
  query: ""
};

export function suggestedSeries(state = suggestedSeriesInitialState, action) {
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
    case actions.RESET_SUGGESTED_SERIES:
      return suggestedSeriesInitialState;
    case actions.SUGGESTED_SERIES_ERROR:
      return { ...selectedSerieInitialState, error: action.error };
    default:
      return state;
  }
}

const selectedSerieInitialState = {
  isFetching: false,
  serie: { name: "" }
};

export function selectedSerie(state = selectedSerieInitialState, action) {
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
    case actions.RESET_SELECTED_SERIE:
      return selectedSerieInitialState;
    case actions.SELECTED_SERIE_ERROR:
      return { ...selectedSerieInitialState, error: action.error };
    default:
      return state;
  }
}

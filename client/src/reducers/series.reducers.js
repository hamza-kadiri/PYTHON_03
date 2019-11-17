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

const favoriteSeriesInitialState = {
  isFetching: false,
  subscriptions: {},
  series: []
};

export function favoriteSeries(state = favoriteSeriesInitialState, action) {
  switch (action.type) {
    case actions.REQUEST_GET_IS_FAVORITE:
      return { ...state, isFetching: true };
    case actions.SUCCESS_GET_IS_FAVORITE:
      return {
        ...state,
        isFetching: false,
        subscriptions: {
          ...state.subscriptions,
          [action.subscription.serie_id]: action.subscription.is_favorite
        }
      };
    case actions.ERROR_GET_IS_FAVORITE:
      return {
        ...state,
        isFetching: false,
        subscriptions: {
          ...state.subscriptions,
          [action.error.serie_id]: action.error
        }
      };
    case actions.REQUEST_TOGGLE_FAVORITE:
      return { ...state, isFetching: true };
    case actions.SUCCESS_TOGGLE_FAVORITE:
      return {
        ...state,
        isFetching: false,
        subscriptions: {
          ...state.subscriptions,
          [action.subscription.serie_id]: action.subscription.is_favorite
        }
      };
    case actions.ERROR_TOGGLE_FAVORITE:
      return {
        ...state,
        isFetching: false,
        subscriptions: {
          ...state.subscriptions,
          [action.error.serie_id]: action.error
        }
      };
    case actions.REQUEST_GET_ALL_FAVORITE:
      return { ...state, isFetching: true };
    case actions.SUCCESS_GET_ALL_FAVORITE:
      return {
        ...state,
        isFetching: false,
        series: action.series,
        subscriptions: {
          ...state.subscriptions,
          ...action.series
            .map(serie => serie.tmdb_id_serie)
            .reduce((acc, id_serie) => ({ ...acc, [id_serie]: true }), {})
        }
      };
    case actions.ERROR_GET_ALL_FAVORITE:
      return {
        ...state,
        isFetching: false
      };
    default:
      return state;
  }
}

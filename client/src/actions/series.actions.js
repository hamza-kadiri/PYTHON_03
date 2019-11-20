import clientWeb from "../helpers/clientWeb";
import { handleError } from "./common.actions";
import { getNotifications } from "./notifications.actions";
export const actions = {
  REQUEST_SUGGESTED_SERIES: "REQUEST_SUGGESTED_SERIES",
  RECEIVE_SUGGESTED_SERIES: "RECEIVE_SUGGESTED_SERIES",
  SUGGESTED_SERIES_ERROR: "SUGGESTED_SERIES_ERROR",
  RESET_SUGGESTED_SERIES: "RESET_SUGGESTED_SERIES",
  REQUEST_SERIE: "REQUEST_SERIE",
  RECEIVE_SERIE: "RECEIVE_SERIE",
  SELECTED_SERIE_ERROR: "SELECTED_SERIE_ERROR",
  RESET_SELECTED_SERIE: "RESET_SELECTED_SERIE",
  REQUEST_TOGGLE_FAVORITE: "REQUEST_TOGGLE_FAVORITE",
  SUCCESS_TOGGLE_FAVORITE: "SUCCESS_TOGGLE_FAVORITE",
  ERROR_TOGGLE_FAVORITE: "ERROR_TOGGLE_FAVORITE",
  REQUEST_GET_ALL_FAVORITE: "REQUEST_GET_ALL_FAVORITE",
  SUCCESS_GET_ALL_FAVORITE: "SUCCESS_GET_ALL_FAVORITE",
  ERROR_GET_ALL_FAVORITE: "ERROR_GET_ALL_FAVORITE",
  REQUEST_GET_IS_FAVORITE: "REQUEST_GET_IS_FAVORITE",
  SUCCESS_GET_IS_FAVORITE: "SUCCESS_GET_IS_FAVORITE",
  ERROR_GET_IS_FAVORITE: "ERROR_GET_IS_FAVORITE",
  REQUEST_DISCOVER_SERIES: "REQUEST_DISCOVER_SERIES",
  SUCCESS_DISCOVER_SERIES: "SUCCESS_DISCOVER_SERIES",
  ERROR_DISCOVER_SERIES: "ERROR_DISCOVER_SERIES"
};

const requestSuggestedSeries = query => {
  return {
    type: actions.REQUEST_SUGGESTED_SERIES,
    query
  };
};

const receiveSuggestedSeries = (query, series) => {
  return {
    type: actions.RECEIVE_SUGGESTED_SERIES,
    query,
    series: series,
    receivedAt: Date.now()
  };
};

export const fetchSuggestedSeries = query => {
  return async dispatch => {
    if (query === "") {
      dispatch({ type: actions.RESET_SUGGESTED_SERIES });
    } else {
      dispatch(requestSuggestedSeries(query));
      try {
        const response = await clientWeb("search", {
          searchParams: { query }
        });
        const json = await response.json();
        dispatch(receiveSuggestedSeries(query, json.results));
      } catch (error) {
        dispatch(handleError(error, actions.SUGGESTED_SERIES_ERROR));
      }
    }
  };
};

const requestSerie = serie_id => {
  return {
    type: actions.REQUEST_SERIE,
    serie_id
  };
};

const receiveSelectedSerie = (serie_id, serie) => {
  return {
    type: actions.RECEIVE_SERIE,
    serie_id,
    serie: serie,
    receivedAt: Date.now()
  };
};

export const fetchSelectedSerie = serie_id => {
  return async dispatch => {
    dispatch(requestSerie(serie_id));
    try {
      const response = await clientWeb(`series/${serie_id}`);
      const json = await response.json();
      dispatch(receiveSelectedSerie(serie_id, json));
    } catch (error) {
      dispatch(handleError(error, actions.SELECTED_SERIE_ERROR));
    }
  };
};

const requestFavorite = (type, user_id, serie_id) => {
  return {
    type,
    user_id,
    serie_id
  };
};

const receiveFavorite = (type, response) => {
  return {
    type,
    subscription: response
  };
};

const requestAllFavorite = user_id => {
  return {
    type: actions.REQUEST_GET_ALL_FAVORITE,
    user_id
  };
};

const receiveAllFavorite = response => {
  return {
    type: actions.SUCCESS_GET_ALL_FAVORITE,
    series: response.series
  };
};

export const toggleFavorite = (user_id, serie_id) => {
  return async dispatch => {
    dispatch(
      requestFavorite(actions.REQUEST_TOGGLE_FAVORITE, user_id, serie_id)
    );
    try {
      const response = await clientWeb.post(`favorite`, {
        json: { user_id, serie_id }
      });

      const json = await response.json();
      dispatch(receiveFavorite(actions.SUCCESS_TOGGLE_FAVORITE, json));
      dispatch(getNotifications(user_id));
    } catch (error) {
      dispatch(handleError(error, actions.ERROR_TOGGLE_FAVORITE));
    }
  };
};

export const getIsFavorite = (user_id, serie_id) => {
  return async dispatch => {
    dispatch(
      requestFavorite(actions.REQUEST_GET_IS_FAVORITE, user_id, serie_id)
    );
    try {
      const response = await clientWeb.get(`favorite`, {
        searchParams: { user_id, serie_id }
      });
      const json = await response.json();
      dispatch(receiveFavorite(actions.SUCCESS_GET_IS_FAVORITE, json));
    } catch (error) {
      dispatch(handleError(error, actions.ERROR_GET_IS_FAVORITE));
    }
  };
};

export const getAllFavorite = user_id => {
  return async dispatch => {
    dispatch(requestAllFavorite(user_id));
    try {
      const response = await clientWeb(`users/${user_id}/series`);
      const json = await response.json();
      dispatch(receiveAllFavorite(json));
    } catch (error) {
      dispatch(handleError(error, actions.ERROR_GET_ALL_FAVORITE));
    }
  };
};

const requestDiscoverSeries = () => {
  return {
    type: actions.REQUEST_DISCOVER_SERIES
  };
};

const receiveDiscoverSeries = response => {
  return {
    type: actions.SUCCESS_DISCOVER_SERIES,
    categories: response
  };
};

export const getDiscoverSeries = () => {
  return async dispatch => {
    dispatch(requestDiscoverSeries());
    try {
      const response = await clientWeb(`discover`);
      const json = await response.json();
      dispatch(receiveDiscoverSeries(json));
    } catch (error) {
      dispatch(handleError(error, actions.ERROR_DISCOVER_SERIES));
    }
  };
};

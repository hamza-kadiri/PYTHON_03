import ky from "ky";

export const REQUEST_SUGGESTED_SERIES = "REQUEST_SUGGESTED_SERIES";

const requestSuggestedSeries = query => {
  return {
    type: REQUEST_SUGGESTED_SERIES,
    query
  };
};

export const RECEIVE_SUGGESTED_SERIES = "RECEIVE_SUGGESTED_SERIES";

const receiveSuggestedSeries = (query, series) => {
  return {
    type: RECEIVE_SUGGESTED_SERIES,
    query,
    series: series,
    receivedAt: Date.now()
  };
};

export const fetchSuggestedSeries = query => {
  return async dispatch => {
    dispatch(requestSuggestedSeries(query));
    const response = await ky.get("//localhost:8001/search", {
      searchParams: { query }
    });
    const json = await response.json();
    dispatch(receiveSuggestedSeries(query, json.results));
  };
};

export const REQUEST_SERIE = "REQUEST_SERIE";

const requestSerie = id_serie => {
  return {
    type: REQUEST_SERIE,
    id_serie
  };
};

export const RECEIVE_SERIE = "RECEIVE_SERIE";

const receiveSelectedSerie = (id_serie, serie) => {
  return {
    type: RECEIVE_SERIE,
    id_serie,
    serie: serie,
    receivedAt: Date.now()
  };
};

export const fetchSelectedSerie = id_serie => {
  return async dispatch => {
    dispatch(requestSerie(id_serie));
    const response = await ky.get(`//localhost:8001/serie/${id_serie}`);
    const json = await response.json();
    dispatch(receiveSelectedSerie(id_serie, json));
  };
};

export const RESET_SERIE = "RESET_SERIE";

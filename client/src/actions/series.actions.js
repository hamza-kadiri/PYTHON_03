import clientWeb from "../helpers/clientWeb";
export const actions = {
  REQUEST_SUGGESTED_SERIES: "REQUEST_SUGGESTED_SERIES",
  RECEIVE_SUGGESTED_SERIES: "RECEIVE_SUGGESTED_SERIES",
  REQUEST_SERIE: "REQUEST_SERIE",
  RECEIVE_SERIE: "RECEIVE_SERIE",
  RESET_SERIE: "RESET_SERIE"
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
    dispatch(requestSuggestedSeries(query));
    const response = await clientWeb("search", {
      searchParams: { query }
    });
    const json = await response.json();
    dispatch(receiveSuggestedSeries(query, json.results));
  };
};

const requestSerie = id_serie => {
  return {
    type: actions.REQUEST_SERIE,
    id_serie
  };
};

const receiveSelectedSerie = (id_serie, serie) => {
  return {
    type: actions.RECEIVE_SERIE,
    id_serie,
    serie: serie,
    receivedAt: Date.now()
  };
};

export const fetchSelectedSerie = id_serie => {
  return async dispatch => {
    dispatch(requestSerie(id_serie));
    try {
      const response = await clientWeb(`series/${id_serie}`);
      const json = await response.json();
      dispatch(receiveSelectedSerie(id_serie, json));
    } catch (err) {
      console.log(err);
    }
  };
};

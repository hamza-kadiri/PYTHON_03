import ky from "ky";

export const actions = {
  REQUEST_SUGGESTED_SERIES: "REQUEST_SUGGESTED_SERIES",
  RECEIVE_SUGGESTED_SERIES: "RECEIVE_SUGGESTED_SERIES",
  REQUEST_SERIE: "REQUEST_SERIE",
  RECEIVE_SERIE: "RECEIVE_SERIE",
  RESET_SERIE: "RESET_SERIE",
  REQUEST_USER_SIGNUP: "REQUEST_USER_SIGNUP",
  USER_SIGNUP_ERROR: "USER_SIGNUP_ERROR",
  REQUEST_USER_TOKEN: "REQUEST_USER_TOKEN",
  RECEIVE_USER_TOKEN: "RECEIVE_USER_TOKEN",
  USER_TOKEN_ERROR: "USER_TOKEN_ERROR"
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
    const response = await ky.get("//localhost:8001/search", {
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
      const response = await ky.get(`//localhost:8001/serie/${id_serie}`);
      const json = await response.json();
      dispatch(receiveSelectedSerie(id_serie, json));
    } catch (err) {
      console.log(err);
    }
  };
};

export const REQUEST_USER_TOKEN = "REQUEST_USER_TOKEN";

const requestUserToken = user => {
  return {
    type: actions.REQUEST_USER_TOKEN,
    user
  };
};

const receiveUserToken = response => {
  return {
    type: actions.RECEIVE_USER_TOKEN,
    response,
    receivedAt: Date.now()
  };
};

export const userSignup = user => {
  return async dispatch => {
    try {
      const response = await ky.post(`//localhost:8001/users`, { json: user });
      const json = await response.json();
      dispatch(userLogin(user));
    } catch (error) {
      console.log(error.response);
      const error_response = await error.response.json();
      dispatch({ type: actions.USER_SIGNUP_ERROR, error: error_response });
    }
  };
};

export const userLogin = user => {
  return async dispatch => {
    try {
      dispatch(requestUserToken(user));
      const response = await ky.post(`//localhost:8001/token`, { json: user });
      const json = await response.json();
      dispatch(receiveUserToken(json));
    } catch (error) {
      console.log(error.response);
      const error_response = await error.response.json();
      dispatch({ type: actions.USER_TOKEN_ERROR, error: error_response });
    }
  };
};

import { suggestedSeries, selectedSerie } from "./series.reducers.js";
import { user } from "./user.reducers.js";
import { combineReducers } from "redux";
import { routerReducer } from "react-router-redux";

const rootReducer = combineReducers({
  routing: routerReducer,
  suggestedSeries,
  selectedSerie,
  user
});

export default rootReducer;

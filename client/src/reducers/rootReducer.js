import { suggestedSeries, selectedSerie } from "./series.reducers.js";
import { user } from "./user.reducers.js";
import { combineReducers } from "redux";

const rootReducer = combineReducers({
  suggestedSeries,
  selectedSerie,
  user
});

export default rootReducer;

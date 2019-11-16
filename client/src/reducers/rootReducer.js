import { suggestedSeries, selectedSerie } from "./series.reducers";
import { user } from "./auth.reducer";
import { signup } from "./signup.reducer";
import { combineReducers } from "redux";

const rootReducer = combineReducers({
  suggestedSeries,
  selectedSerie,
  user,
  signup
});

export default rootReducer;

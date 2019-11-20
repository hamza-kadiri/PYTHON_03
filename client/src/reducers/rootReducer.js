import {
  suggestedSeries,
  selectedSerie,
  favoriteSeries,
  discoverSeries
} from "./series.reducers";
import { user } from "./auth.reducer";
import { signup } from "./signup.reducer";
import { notifications } from "./notificiations.reducer";
import { combineReducers } from "redux";

const allReducers = combineReducers({
  suggestedSeries,
  selectedSerie,
  favoriteSeries,
  discoverSeries,
  user,
  signup,
  notifications
});

const rootReducer = (state, action) => {
  if (action.type === "RESET_APP") {
    state = undefined;
  }
  return allReducers(state, action);
};

export default rootReducer;

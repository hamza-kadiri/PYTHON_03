import {
  suggestedSeries,
  selectedSerie,
  favoriteSeries
} from "./series.reducers";
import { user } from "./auth.reducer";
import { signup } from "./signup.reducer";
import { notifications } from "./notificiations.reducer";
import { combineReducers } from "redux";

const rootReducer = combineReducers({
  suggestedSeries,
  selectedSerie,
  favoriteSeries,
  user,
  signup,
  notifications
});

export default rootReducer;

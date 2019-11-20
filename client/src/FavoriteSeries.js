import React, { useEffect } from "react";
import { getAllFavorite } from "./actions/series.actions";
import { connect, useDispatch } from "react-redux";
import FavoriteSerie from "./FavoriteSerie";
import { CircularProgress } from "@material-ui/core";

const FavoriteSeries = ({ user, series, isFetching }) => {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(getAllFavorite(user.id));
  }, [user, dispatch]);
  return isFetching ? (
    <CircularProgress
      style={{
        position: "absolute",
        margin: "auto",
        left: 0,
        right: 0,
        top: 0,
        bottom: 0
      }}
      size={50}
      color="primary"
    />
  ) : (
    <React.Fragment>
      <div
        style={{
          alignItems: "flex-start",
          paddingTop: "4rem",
          height: "calc(100vh - 4rem)",
          width: "100%",
          flexDirection: "column"
        }}
      >
        <React.Fragment>
          {series.map((serie, index) => (
            <React.Fragment key={index}>
              <FavoriteSerie serie={serie}></FavoriteSerie>
            </React.Fragment>
          ))}
        </React.Fragment>
      </div>
    </React.Fragment>
  );
};

const mapStateToProps = ({ favoriteSeries, user }) => {
  return {
    series: favoriteSeries.series,
    isFetching: favoriteSeries.isFetching,
    user: user.user
  };
};
export default connect(mapStateToProps)(FavoriteSeries);

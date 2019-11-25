import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CircularProgress from "@material-ui/core/CircularProgress";
import Chip from "@material-ui/core/Chip";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import LikeIcon from "@material-ui/icons/Favorite";
import OutlinedLikeIcon from "@material-ui/icons/FavoriteBorder";
import React, { useEffect } from "react";
import { connect, useDispatch } from "react-redux";
import {
  fetchSelectedSerie,
  getIsFavorite,
  toggleFavorite
} from "./actions/series.actions";

const useStyles = makeStyles(theme => ({
  LikeIcon: {
    marginRight: theme.spacing(1)
  }
}));

const Serie = ({
  match,
  serie,
  isLoading,
  user,
  subscriptions,
  isLoadingSubscriptions
}) => {
  const classes = useStyles();
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(fetchSelectedSerie(match.params.id));
    dispatch(getIsFavorite(user.id, match.params.id));
  }, [match.params.id, dispatch, user.id]);

  const handleLike = async () => {
    await dispatch(toggleFavorite(user.id, serie.id));
  };

  return (
    <React.Fragment>
      <div
        style={{
          background: "rgb(0, 0, 0)",
          backgroundImage: `linear-gradient(
                to right,
                rgba(0,0,0, 100) 15%,
                rgba(0,0,0, 0) 100%
              ), url(${serie.backdrop_url})`,
          backgroundSize: "cover",
          position: "absolute",
          height: "100vh",
          width: "100%",
          top: 0,
          zIndex: 1
        }}
      ></div>
      <div
        style={{
          position: "absolute",
          display: "flex",
          width: "100%",
          height: "100%",
          alignItems: "center",
          zIndex: 2
        }}
      >
        <Card
          elevation={0}
          style={{
            height: "80%",
            width: "25%",
            color: "white",
            background: `rgba(0,0,0,0)`
          }}
        >
          <CardContent>
            {isLoading || serie.name == "" ? (
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
                <Typography variant="h3">
                  {serie.name}{" "}
                  {serie.in_production ? (
                    <Chip
                      color="primary"
                      label="In production"
                      style={{ color: "white", fontWeight: "bold" }}
                    />
                  ) : (
                    <Chip
                      variant="outlined"
                      color="primary"
                      style={{ color: "white", fontWeight: "bold" }}
                      label="Finished"
                    />
                  )}
                </Typography>
                <Typography variant="h6" style={{ paddingLeft: 5 }}>
                  {new Date(serie.last_air_date).getFullYear()}
                  {serie.seasons.length > 0 &&
                    ` - ${serie.seasons.length} Seasons  `}
                </Typography>
                <Typography
                  gutterBottom
                  variant="h6"
                  style={{ paddingLeft: 5 }}
                >
                  {serie.next_episode_to_air &&
                    `Next Episode: S${serie.next_episode_to_air.season_number} E${serie.next_episode_to_air.episode_number}`}
                </Typography>
                <Button
                  variant={
                    subscriptions[match.params.id] ? "contained" : "outlined"
                  }
                  color="primary"
                  onClick={handleLike}
                  style={{ width: "50%", minWidth: "200px", marginBottom: 10 }}
                >
                  {isLoadingSubscriptions ? (
                    <CircularProgress
                      size={20}
                      className={classes.LikeIcon}
                      color="primary"
                    />
                  ) : subscriptions[match.params.id] ? (
                    <LikeIcon className={classes.LikeIcon} />
                  ) : (
                    <OutlinedLikeIcon className={classes.LikeIcon} />
                  )}
                  {subscriptions[match.params.id]
                    ? "Remove Favorite"
                    : "Favorite"}
                </Button>
                {serie.genres.length > 0 && (
                  <Typography variant="body1" gutterBottom>
                    <b>Genres: </b>
                    {serie.genres.map(
                      (genre, index) => (index ? ", " : "") + genre.name
                    )}
                  </Typography>
                )}
                {serie.created_by.length > 0 && (
                  <Typography variant="body1" gutterBottom>
                    <b>Producers: </b>
                    {serie.created_by.map(
                      (person, index) => (index ? ", " : "") + person.name
                    )}
                  </Typography>
                )}
                {serie.overview && (
                  <Typography variant="body1" gutterBottom>
                    <b>Overview: </b>
                    {serie.overview}
                  </Typography>
                )}
              </React.Fragment>
            )}
          </CardContent>
        </Card>
      </div>
    </React.Fragment>
  );
};

const mapStateToProps = ({ selectedSerie, user, favoriteSeries }) => ({
  serie: selectedSerie.serie,
  isLoading: selectedSerie.isFetching,
  user: user.user,
  subscriptions: favoriteSeries.subscriptions,
  isLoadingSubscriptions: favoriteSeries.isFetching
});

export default connect(mapStateToProps)(Serie);

import React from "react";
import IconCross from "./IconCross";
import "./Content.scss";
import { Button, Grid, IconButton } from "@material-ui/core";
import { Link } from "react-router-dom";
import { fade, makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(theme => {
  return {
    search: {
      position: "relative",
      borderRadius: theme.shape.borderRadius,
      opacity: 1,
      backgroundColor: fade(theme.palette.common.white, 0.15),
      "&:hover": {
        backgroundColor: fade(theme.palette.common.white, 0.25)
      },
      marginRight: theme.spacing(2),
      marginLeft: 0,
      width: "70%",
      [theme.breakpoints.up("sm")]: {
        marginLeft: theme.spacing(3)
      }
    },
    content: {
      display: "flex",
      width: "100%"
    },
    backgroundShadow: {
      left: "0",
      background: "#000",
      width: "35%",
      zIndex: "2",
      position: "absolute",
      height: "37vh",
      "&:before": {
        content: '""',
        position: "absolute",
        zIndex: "10",
        backgroundImage: "linear-gradient(to right, #000, transparent)",
        top: "0",
        bottom: "0",
        left: "100%",
        width: "275px"
      }
    },
    backgroundImage: {
      right: "0",
      width: "65%",
      backgroundPosition: "center 10%",
      backgroundSize: "cover",
      zIndex: "1",
      position: "absolute",
      height: "37vh"
    },
    background: { left: "0", right: "0" },
    contentArea: {
      left: "0",
      right: "0",
      height: "37vh",
      width: "100%",
      zIndex: "3"
    },
    contentAreaContainer: { padding: "20px 10px 0px 30px", color: "wheat" },
    contentTitle: { fontSize: "45px", color: "#fff", fontWeight: "700" },
    contentTitleEpisode: { fontSize: "32px", color: "#fff", fontWeight: "700" },
    contentSubTitleEpisode: {
      fontSize: "24px",
      color: "#ccc",
      fontWeight: "500"
    },
    contentDescription: {
      fontSize: "18px",
      color: "#999",
      marginTop: "20px",
      maxWidth: "500px",
      overflow: "hidden",
      display: "-webkit-box",
      WebkitLineClamp: "15",
      WebkitBoxOrient: "vertical",
      flex: "1",
      maxHeight: "15vh"
    }
  };
});
const Content = ({ serie, onClose, singleSlider, episode, refProp }) => {
  const classes = useStyles();
  const singleSliderStyle = { height: "100vh", position: "fixed" };
  const backgroundImage = episode
    ? `url(${serie.still_url})`
    : `url(${serie.thumbnail_url})`;
  return (
    <div ref={refProp} className={classes.content}>
      <div className={classes.background}>
        <div
          className={classes.backgroundShadow}
          style={singleSlider && singleSliderStyle}
        />
        <div
          className={classes.backgroundImage}
          style={
            singleSlider
              ? {
                  backgroundImage: backgroundImage,
                  ...singleSliderStyle
                }
              : {
                  backgroundImage: backgroundImage
                }
          }
        />
      </div>
      <div
        className={classes.contentArea}
        style={singleSlider && { height: "100%" }}
      >
        <div className={classes.contentAreaContainer}>
          <Grid container justify="space-between">
            <Grid
              container
              item
              alignItems="flex-start"
              sm={4}
              direction="column"
            >
              <Grid item>
                <div
                  className={
                    episode ? classes.contentTitleEpisode : classes.contentTitle
                  }
                >
                  {serie.name}
                </div>
              </Grid>
              {episode ? (
                <div className={classes.contentSubTitleEpisode}>
                  Season {serie.season_number} - Episode {serie.episode_number}
                </div>
              ) : (
                <Grid item>
                  <div>
                    <Button
                      component={Link}
                      to={`/serie/${serie.id}`}
                      variant="outlined"
                      color="primary"
                    >
                      More Details
                    </Button>
                  </div>
                </Grid>
              )}
              <Grid item>
                <div className={classes.contentDescription}>
                  {serie.overview}
                </div>
              </Grid>
            </Grid>
            <Grid item>
              <IconButton style={{ color: "white" }} onClick={onClose}>
                <IconCross />
              </IconButton>
            </Grid>
          </Grid>
        </div>
      </div>
    </div>
  );
};

export default Content;

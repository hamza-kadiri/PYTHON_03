import React from "react";
import IconCross from "./IconCross";
import "./Content.scss";
import { Button, Grid } from "@material-ui/core";
import { Link } from "react-router-dom";

const Content = ({ serie, onClose }) => (
  <div className="content">
    <div className="content__background">
      <div className="content__background__shadow" />
      <div
        className="content__background__image"
        style={{
          background: `linear-gradient(
            to bottom,
            rgba(0,0,0, 20),
            rgba(0,0,0, 0) 95%,
            rgba(0,0,0, 10)
          ), url(${serie.thumbnail_url})`
        }}
      />
    </div>
    <div className="content__area">
      <div className="content__area__container">
        <Grid container alignItems="center" sm={4} justify="space-between">
          <Grid item>
            <div className="content__title">{serie.name}</div>
          </Grid>
          <Grid item>
            <div className="content__details">
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
        </Grid>
        <div className="content__description">{serie.overview}</div>
      </div>
      <button className="content__close" onClick={onClose}>
        <IconCross />
      </button>
    </div>
  </div>
);

export default Content;

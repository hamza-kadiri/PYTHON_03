import React from "react";
import cx from "classnames";
import SliderContext from "./context";
import "./SerieThumbnail.scss";
import Mark from "./Mark";
import ShowDetailsButton from "./ShowDetailsButton";
import { Button } from "@material-ui/core";

const SerieThumbnail = ({ serie }) => (
  <SliderContext.Consumer>
    {({ onSelectSlide, currentSlide, elementRef }) => {
      const isActive = currentSlide && currentSlide.id === serie.id;

      return (
        <div
          ref={elementRef}
          className={cx("item", {
            "item--open": isActive
          })}
        >
          <img
            onClick={() => onSelectSlide(serie)}
            className="img"
            src={serie.poster_url}
            alt=""
          />
          <ShowDetailsButton onClick={() => onSelectSlide(serie)} />
          {isActive && <Mark />}
          <div
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              bottom: 1,
              margin: "auto",
              color: "black"
            }}
            variant="outlined"
            color="primary"
          >
            Test
          </div>
        </div>
      );
    }}
  </SliderContext.Consumer>
);

export default SerieThumbnail;

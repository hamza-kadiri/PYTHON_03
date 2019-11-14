import cx from "classnames";
import React from "react";
import SliderContext from "./context";
import Mark from "./Mark";
import "./SerieThumbnail.scss";
import ShowDetailsButton from "./ShowDetailsButton";

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
        </div>
      );
    }}
  </SliderContext.Consumer>
);

export default SerieThumbnail;

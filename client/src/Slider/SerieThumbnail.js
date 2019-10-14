import React from "react";
import cx from "classnames";
import SliderContext from "./context";
import "./SerieThumbnail.scss";

const SerieThumbnail = ({ serie }) => (
  <SliderContext.Consumer>
    {({ currentSlide, elementRef }) => {
      const isActive = currentSlide && currentSlide.id === serie.id;

      return (
        <div
          ref={elementRef}
          className={cx("item", {
            "item--open": isActive
          })}
        >
          <img className="img" src={serie.poster_url} alt="" />
        </div>
      );
    }}
  </SliderContext.Consumer>
);

export default SerieThumbnail;

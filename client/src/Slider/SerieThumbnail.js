import cx from "classnames";
import React, { useState } from "react";
import SliderContext from "./context";
import Mark from "./Mark";
import "./SerieThumbnail.scss";
import ShowDetailsButton from "./ShowDetailsButton";

const SerieThumbnail = ({ serie }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <SliderContext.Consumer>
      {({ onSelectSlide, onHoverSlide, currentSlide, elementRef }) => {
        const isActive = currentSlide && currentSlide.id === serie.id;
        const handleClick = serie => {
          setIsHovered(false);
          onSelectSlide(serie);
        };
        const background =
          currentSlide || isHovered
            ? isActive || isHovered
              ? "linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.9))"
              : "rgba(0, 0, 0, 0.6)"
            : "rgba(0, 0, 0, 0)";
        return (
          <div
            ref={elementRef}
            className={cx("item", {
              "item--open": isActive
            })}
            onMouseEnter={() =>
              setTimeout(() => !currentSlide && setIsHovered(true), 100)
            }
            onMouseLeave={() =>
              setTimeout(() => !currentSlide && setIsHovered(false), 100)
            }
          >
            <img
              className="img"
              src={serie.poster_url || serie.thumbnail_url}
              alt=""
            />
            <div
              onClick={() => handleClick(serie)}
              style={{
                position: "absolute",
                height: "100%",
                width: "100%",
                top: 0,
                background: background
              }}
            ></div>
            {(isActive || isHovered) && (
              <React.Fragment>
                <div
                  style={{
                    position: "absolute",
                    bottom: "20px",
                    right: "16px",
                    left: "10px",
                    lineHeight: 1.4,
                    fontWeight: "bold",
                    textShadow: "0 1px 1px rgba(0, 0, 0, 0.7)",
                    textOverflow: "ellipsis",
                    overflow: "hidden"
                  }}
                >
                  {serie.name}
                </div>
              </React.Fragment>
            )}

            <ShowDetailsButton
              onClick={() => {
                handleClick(serie);
              }}
            />
            {isActive && <Mark />}
          </div>
        );
      }}
    </SliderContext.Consumer>
  );
};

export default SerieThumbnail;

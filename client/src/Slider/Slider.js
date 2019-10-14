import React, { useState } from "react";
import cx from "classnames";
import SliderContext from "./context";
import SlideButton from "./SlideButton";
import SliderWrapper from "./SliderWrapper";
import useSliding from "./useSliding";
import useSizeElement from "./useSizeElement";
import "./Slider.scss";

const Slider = ({ children, activeSlide }) => {
  const [currentSlide, setCurrentSlide] = useState(activeSlide);
  const { width, elementRef } = useSizeElement();
  const {
    handlePrev,
    handleNext,
    slideProps,
    containerRef,
    hasNext,
    hasPrev
  } = useSliding(width, React.Children.count(children));

  const handleSelect = movie => {
    setCurrentSlide(movie);
  };

  const handleClose = () => {
    setCurrentSlide(null);
  };

  const contextValue = {
    onSelectSlide: handleSelect,
    onCloseSlide: handleClose,
    elementRef,
    currentSlide
  };

  return (
    <SliderContext.Provider value={contextValue}>
      <SliderWrapper>
        <div
          ref={containerRef}
          className={cx("slider", { "slider--open": currentSlide != null })}
        >
          <div className="slider__container" {...slideProps}>
            {children}
          </div>
        </div>
        {hasPrev && <SlideButton onClick={handlePrev} type="prev" />}
        {hasNext && <SlideButton onClick={handleNext} type="next" />}
      </SliderWrapper>
    </SliderContext.Provider>
  );
};

export default Slider;

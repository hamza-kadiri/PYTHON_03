import cx from "classnames";
import React, { useState } from "react";
import Content from "./Content";
import SliderContext from "./context";
import SlideButton from "./SlideButton";
import "./Slider.scss";
import SliderWrapper from "./SliderWrapper";
import useSizeElement from "./useSizeElement";
import useSliding from "./useSliding";

const Slider = ({ children, activeSlide }) => {
  const [currentSlide, setCurrentSlide] = useState(activeSlide);
  let { width, elementRef } = useSizeElement();
  let {
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
      {currentSlide && <Content serie={currentSlide} onClose={handleClose} />}
    </SliderContext.Provider>
  );
};

export default Slider;

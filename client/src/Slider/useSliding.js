import { useState, useRef, useEffect } from "react";

const useSliding = (elementWidth, countElements) => {
  const containerRef = useRef(null);
  const [containerWidth, setContainerWidth] = useState(0);
  const [distance, setDistance] = useState(0);
  const [totalInViewport, setTotalInViewport] = useState(0);
  const [viewed, setViewed] = useState(0);

  useEffect(() => {
    if (containerRef.current != null) {
      const containerWidth = containerRef.current.clientWidth;
      setContainerWidth(containerWidth);
      setTotalInViewport(Math.floor(containerWidth / elementWidth));
    }
  }, [elementWidth]);

  const handlePrev = () => {
    setViewed(viewed - totalInViewport);
    setDistance(distance + containerWidth);
  };

  const handleNext = () => {
    setViewed(viewed + totalInViewport);
    setDistance(distance - containerWidth);
  };

  const slideProps = {
    style: { transform: `translate3d(${distance}px, 0, 0)` }
  };

  const hasPrev = distance < 0;
  const hasNext = viewed + totalInViewport < countElements;

  return { handlePrev, handleNext, slideProps, containerRef, hasPrev, hasNext };
};

export default useSliding;

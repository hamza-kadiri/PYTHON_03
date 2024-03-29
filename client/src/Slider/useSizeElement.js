import { useState, useRef, useEffect } from "react";

const useSizeElement = () => {
  const elementRef = useRef(null);
  const [width, setWidth] = useState(0);

  useEffect(() => {
    if (elementRef.current != null) {
      setWidth(elementRef.current.clientWidth);
    }
  }, [elementRef]);

  return { width, elementRef };
};

export default useSizeElement;

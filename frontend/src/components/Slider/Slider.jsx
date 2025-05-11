import React, { useState, useRef, useEffect } from "react";
import "./Slider.scss";

const Slider = ({ handleChangePriority, name = "slider", initValue = 10 }) => {
  const [value, setValue] = useState(initValue);
  const [inputWidth, setInputWidth] = useState(0);
  const [thumbPos, setThumbPos] = useState(15);
  const inputRef = useRef(null);

  const updateThumbPos = (newValue, newInputWidth) => {
    const max = 10;
    const thumbWidth = 30;
    const rangeWidth = newInputWidth - thumbWidth;
    const posX = (newValue / max) * rangeWidth + thumbWidth / 2;
    setThumbPos(posX);
  };

  const handleChange = (event) => {
    handleChangePriority(event);
    const newValue = event.target.value;
    setValue(newValue);
    updateThumbPos(newValue, inputWidth);
  };

  useEffect(() => {
    if (inputRef.current) {
      const newInputWidth = inputRef.current.offsetWidth;
      setInputWidth(newInputWidth);
      updateThumbPos(value, newInputWidth);
    }

    const handleResize = () => {
      if (inputRef.current) {
        const newInputWidth = inputRef.current.offsetWidth;
        setInputWidth(newInputWidth);
        updateThumbPos(value, newInputWidth);
      }
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [value]);

  useEffect(() => {
    setValue(initValue);
  }, [initValue]);

  return (
    <div className="slider-container">
      <input
        type="range"
        min="0"
        max="10"
        step="1"
        value={value}
        onChange={handleChange}
        className="slider"
        style={{
          background: `linear-gradient(to right, #7c9cc0 ${
            value * 10
          }%, #cdcfd2 ${value * 10}%)`,
        }}
        ref={inputRef}
        name={name}
      />
      <p
        className="value"
        style={{
          transform: `translateX(${thumbPos - 6 + 2}px)`,
        }}
      >
        {value}
      </p>
    </div>
  );
};

export default Slider;

import React from "react";
import { HuePicker, TwitterPicker } from "react-color";
import "./ColorPicker.scss";
const ColorPicker = ({ currentColor, setCurrentColor }) => {
  const customColors = [
    "#000000",
    "#FFFFFF",
    "#FF6900",
    "#FCB900",
    "#7BDCB5",
    "#00D084",
    "#8ED1FC",
    "#0693E3",
    "#ABB8C3",
    "#EB144C",
    "#F78DA7",
    "#9900EF",
  ];
  const handleOnChangeComplete = (color) => {
    setCurrentColor(color.hex);
  };

  const handleOnChange = (color) => {
    setCurrentColor(color.hex);
  };

  return (
    <div className="color-picker">
      <div
        className="current-color"
        style={{ backgroundColor: `${currentColor}` }}
      ></div>
      <TwitterPicker
        color={currentColor}
        onChangeComplete={handleOnChangeComplete}
        onChange={handleOnChange}
        colors={customColors}
      />
      <HuePicker
        color={currentColor}
        onChangeComplete={handleOnChangeComplete}
        onChange={handleOnChange}
      />
    </div>
  );
};

export default ColorPicker;

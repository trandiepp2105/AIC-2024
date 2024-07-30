import React from "react";
import "./PickedFrames.scss";
const PickedFrames = ({
  setPickedFrames,
  pickedFrames,
  framesDisplay,
  currentFrameIndex,
  setCurrentFrameIndex,
  handleClickFrameItem,
  handleDoubleClickFrameItem,
  handlePickFrameItem,
}) => {
  return (
    <ul className="picked-frames-container frame-browsing-area">
      {Array.from(pickedFrames).map((frameIndex) => (
        <li
          key={frameIndex}
          className={`frame-item ${
            currentFrameIndex === frameIndex ? "frame-item-selected" : ""
          } ${pickedFrames.has(frameIndex) ? "frame-item-group" : ""}`}
          onClick={(event) => handleClickFrameItem(event, frameIndex)}
          onDoubleClick={() => handleDoubleClickFrameItem(frameIndex)}
        >
          <img
            src={framesDisplay[frameIndex].path}
            alt="img-frame"
            className="img-frame"
          />
          <input
            type="checkbox"
            name={`frame-item-check-${frameIndex}`}
            className="frame-item-checkbox"
            checked={pickedFrames.has(frameIndex)}
            onChange={(event) => handlePickFrameItem(event, frameIndex)}
          />
          <div
            className="cus-checkbox"
            name={`frame-item-cus-check-${frameIndex}`}
          ></div>
        </li>
      ))}
    </ul>
  );
};

export default PickedFrames;

import React, { useState, useRef } from "react";
import "./BrowsingInterface.scss";
import VideoPlayer from "../VideoPlayer/VideoPlayer";
import { useSearchData } from "../../pages/home-page/HomePage";
const BrowsingInterface = () => {
  const [frameSelected, setFrameItemSelected] = useState(null);
  const [groupedFrames, setGroupedFrames] = useState(new Set());
  const [playVideo, setPlayVideo] = useState(false);
  const videoPlayerRef = useRef(null);
  const { searchData, setSearchData } = useSearchData();
  const handleDoubleClickFrameItem = (index) => {
    setGroupedFrames((prevGroupedFrames) => {
      const newGroupedFrames = new Set(prevGroupedFrames);
      if (newGroupedFrames.has(index)) {
        newGroupedFrames.delete(index);
      } else {
        newGroupedFrames.add(index);
      }
      return newGroupedFrames;
    });
  };

  const initialFrameInfor = {
    frameIndex: 0,
    frameName: "frame_0",
    time: 10,
  };

  const [frameInfor, setFrameInfor] = useState(initialFrameInfor);
  const handleClickFrameItem = (event, index) => {
    setFrameItemSelected(index);
    const imgElement = event.target;
    const wrapper = document.getElementById("wrapper-frame-selected");

    if (imgElement && wrapper) {
      const contentDiv = wrapper.querySelector(".content");
      if (contentDiv) {
        const imgClone = imgElement.cloneNode(true);
        contentDiv.innerHTML = "";
        contentDiv.appendChild(imgClone);
      }
    }

    setFrameInfor(frameInfor);
    setPlayVideo(true);
  };

  const handleCloseButton = () => {
    setPlayVideo(!playVideo);
  };
  return (
    <div className="browsing-interface">
      <ul className="frame-browsing-area">
        {Array.from({ length: 50 }).map((_, index) => (
          <li
            key={index}
            className={`frame-item ${
              frameSelected === index ? "frame-item-selected" : ""
            } ${groupedFrames.has(index) ? "frame-item-group" : ""}`}
            onClick={(event) => handleClickFrameItem(event, index)}
            onDoubleClick={() => handleDoubleClickFrameItem(index)}
          >
            <img
              src="https://i.pinimg.com/736x/1f/82/e4/1f82e49178198aca68d3dd000f05acae.jpg"
              alt="img-frame"
              className="img-frame"
            />
          </li>
        ))}
      </ul>
      {playVideo ? (
        <div className="wrapper-video-player" ref={videoPlayerRef}>
          <div className="overlay"></div>
          <div className="close-button" onClick={handleCloseButton}>
            <svg
              width="30px"
              height="30px"
              viewBox="0 0 16 16"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill="#f50"
                fill-rule="evenodd"
                d="M11.2929,3.29289 C11.6834,2.90237 12.3166,2.90237 12.7071,3.29289 C13.0976,3.68342 13.0976,4.31658 12.7071,4.70711 L9.41421,8 L12.7071,11.2929 C13.0976,11.6834 13.0976,12.3166 12.7071,12.7071 C12.3166,13.0976 11.6834,13.0976 11.2929,12.7071 L8,9.41421 L4.70711,12.7071 C4.31658,13.0976 3.68342,13.0976 3.29289,12.7071 C2.90237,12.3166 2.90237,11.6834 3.29289,11.2929 L6.58579,8 L3.29289,4.70711 C2.90237,4.31658 2.90237,3.68342 3.29289,3.29289 C3.68342,2.90237 4.31658,2.90237 4.70711,3.29289 L8,6.58579 L11.2929,3.29289 Z"
              />
            </svg>
          </div>
          <div className="container">
            <VideoPlayer startTime={frameInfor.time} />
          </div>
        </div>
      ) : null}
    </div>
  );
};

export default BrowsingInterface;

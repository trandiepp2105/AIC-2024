import React, { useState, useRef, useEffect } from "react";
import "./BrowsingInterface.scss";
import VideoPlayer from "../VideoPlayer/VideoPlayer";
import LoadingScreen from "react-loading-screen";
import get_video from "../../services/get_video";
import PickedFrames from "../PickedFrames/PickedFrames";

function calculateFrameTime(frameNumber, fps = 25) {
  if (fps <= 0) {
    throw new Error("FPS phải lớn hơn 0");
  }
  const timeInSeconds = frameNumber / fps;
  return timeInSeconds;
}

const BrowsingInterface = ({ frameDisplay, loading = false }) => {
  const [currentFrameIndex, setCurrentFrameIndex] = useState(null);
  const [pickedFrames, setPickedFrames] = useState(new Set());
  const [playVideo, setPlayVideo] = useState(false);

  const initialVideoInfor = { path: "", startTime: 0 };
  const [videoInfor, setVideoInfor] = useState(initialVideoInfor);
  const browsingOptionType = {
    BROWSING: "browsing",
    PICKED: "picked",
  };
  const [browsingOption, setBrowsingOption] = useState(
    browsingOptionType.BROWSING
  );
  const frameBrowsingAreaRef = useRef(null);

  const handleClickFrameItem = (event, index) => {
    setCurrentFrameIndex(index);
  };

  const clearPickedFrames = () => {
    setPickedFrames(new Set());
  };

  const handlePickFrameItem = (event, index) => {
    event.stopPropagation(); // Ngăn chặn sự kiện click lan truyền lên phần tử cha
    console.log("pick frame: ", index);
    setPickedFrames((prevGroupedFrames) => {
      const newGroupedFrames = new Set(prevGroupedFrames);
      if (newGroupedFrames.has(index)) {
        newGroupedFrames.delete(index);
      } else {
        newGroupedFrames.add(index);
      }
      return newGroupedFrames;
    });
  };

  const handleDoubleClickFrameItem = async (index) => {
    try {
      const frame_infor = frameDisplay[index];
      const video_res = await get_video(frame_infor.video_id);
      if (video_res && video_res.status >= 200 && video_res.status < 300) {
        setVideoInfor((prevData) => {
          const newVideoInfor = {
            ...prevData,
            path: video_res.data.path,
            startTime: calculateFrameTime(frame_infor.frame_number),
          };
          return newVideoInfor;
        });
      } else {
        console.error("Error fetching video");
        setVideoInfor(initialVideoInfor);
      }
    } catch (error) {
      console.error("Get video failed:", error);
      setVideoInfor(initialVideoInfor);
    }
    setPlayVideo(true);
  };

  const handleClosePlayerVideo = () => {
    setPlayVideo(false);
  };

  const toggleActiveBrowsingOption = (event) => {
    event.preventDefault();
    if (browsingOption === browsingOptionType.BROWSING) {
      setBrowsingOption(browsingOptionType.PICKED);
    } else {
      setBrowsingOption(browsingOptionType.BROWSING);
    }
  };

  useEffect(() => {
    console.log("picked frames: ", pickedFrames);
  }, [pickedFrames]);

  if (loading) {
    return (
      <div className="browsing-interface">
        <LoadingScreen
          loading={true}
          bgColor="#a8bdb9"
          spinnerColor="#EC7700"
          textColor="#EC7700"
          text="Loading . . ."
        />
      </div>
    );
  }
  return (
    <>
      <div className="browsing-interface">
        {frameDisplay && frameDisplay.length > 0 ? (
          <div className="browsing-option">
            <button
              className={`browsing-frames-btn ${
                browsingOption === browsingOptionType.BROWSING
                  ? "activeBrwosingOption"
                  : null
              }`}
              onClick={() => {
                setBrowsingOption(browsingOptionType.BROWSING);
              }}
            >
              BROWSING FRAME
            </button>
            <div
              className="wrapper-convert-icon"
              onClick={toggleActiveBrowsingOption}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="20"
                width="20"
                viewBox="0 0 512 512"
                version="1.1"
                transform="matrix(6.123233995736766e-17,1,-1,6.123233995736766e-17,0,0)"
              >
                <path
                  stroke-width="20"
                  stroke="black"
                  d="M303.453 170.146c-5.001-5.001-13.099-5.001-18.099 0l-80.555 80.555V12.8c0-7.074-5.726-12.8-12.8-12.8s-12.8 5.726-12.8 12.8v237.901l-80.546-80.546c-5.001-5.001-13.099-5.001-18.099 0-5.001 5.001-5.001 13.099 0 18.099l102.4 102.4c2.5 2.5 5.777 3.746 9.054 3.746s6.554-1.246 9.054-3.746l102.4-102.4c4.983-5.001 4.983-13.107-.009-18.108m128 153.6-102.4-102.4c-2.5-2.5-5.777-3.746-9.054-3.746s-6.554 1.246-9.054 3.746l-102.4 102.4c-5.001 5-5.001 13.099 0 18.099s13.099 5 18.099 0l80.555-80.546V499.2c0 7.074 5.726 12.8 12.8 12.8s12.8-5.726 12.8-12.8V261.299l80.546 80.546c5.001 5.001 13.099 5.001 18.099 0 5.001-5 5.001-13.098.009-18.099"
                ></path>
              </svg>
            </div>
            <button
              className={`browsing-frames-btn ${
                browsingOption === browsingOptionType.PICKED
                  ? "activeBrwosingOption"
                  : null
              }`}
              onClick={() => {
                setBrowsingOption(browsingOptionType.PICKED);
              }}
            >
              PICKED FRAMES
            </button>
            <div className="submit-services">
              <button type="button" className="submit-frames-btn">
                SUBMIT
              </button>
              <button
                type="button"
                className="clear-picked-frames-btn"
                onClick={clearPickedFrames}
              >
                CLEAR PICKED FRAMES
              </button>
            </div>
          </div>
        ) : null}
        {browsingOption === browsingOptionType.BROWSING ? (
          <ul className="frame-browsing-area" ref={frameBrowsingAreaRef}>
            {frameDisplay.map((frame, index) => (
              <li
                key={index}
                className={`frame-item ${
                  currentFrameIndex === index ? "frame-item-selected" : ""
                } ${pickedFrames.has(index) ? "frame-item-group" : ""}`}
                onClick={(event) => handleClickFrameItem(event, index)}
                onDoubleClick={() => handleDoubleClickFrameItem(index)}
              >
                <img src={frame.path} alt="img-frame" className="img-frame" />
                <input
                  type="checkbox"
                  name={`frame-item-check-${index}`}
                  className="frame-item-checkbox"
                  checked={pickedFrames.has(index)}
                  onChange={(event) => handlePickFrameItem(event, index)}
                />
                <div
                  className="cus-checkbox"
                  name={`frame-item-cus-check-${index}`}
                ></div>
              </li>
            ))}
          </ul>
        ) : (
          <PickedFrames
            setPickedFrames={setPickedFrames}
            pickedFrames={pickedFrames}
            framesDisplay={frameDisplay}
            currentFrameIndex={currentFrameIndex}
            setCurrentFrameIndex={setCurrentFrameIndex}
            handleClickFrameItem={handleClickFrameItem}
            handleDoubleClickFrameItem={handleDoubleClickFrameItem}
            handlePickFrameItem={handlePickFrameItem}
          />
        )}
        {playVideo && (
          <div className="wrapper-video-player">
            <div className="overlay"></div>
            <div className="container">
              <VideoPlayer
                startTime={videoInfor.startTime}
                videoPath={videoInfor.path}
                handleClosePlayerVideo={handleClosePlayerVideo}
              />
            </div>
          </div>
        )}{" "}
      </div>
    </>
  );
};

export default BrowsingInterface;

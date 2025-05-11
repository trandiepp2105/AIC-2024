import React, { useState, useRef, useEffect, useCallback } from "react";
import "./BrowsingInterface.scss";
import VideoPlayer from "../VideoPlayer/VideoPlayer";
import LoadingScreen from "react-loading-screen";
import get_video from "../../services/get_video";
import get_video_by_name from "../../services/get_video_by_name";
import PickedFrames from "../PickedFrames/PickedFrames";
import AdjacentFrame from "../AdjacentFrame/AdjacentFrame";
import get_adjacent_frame from "../../services/get_adjacent_frame";
import TeamPickedFrames from "../TeamPickedFrames/TeamPickedFrames";
import getTeamPickedFrames from "../../services/get_team_picked";
import QAInput from "../QAInput/QAInput";
import postTeamPickedFrames from "../../services/upload_to_team_picked";
import { useHomeContext } from "../../pages/home-page/HomePage";
import submit from "../../services/submit";
import {
  NotificationContainer,
  NotificationManager,
} from "react-notifications";
import SubmitConfirm from "../SubmitConfirm/SubmitConfirm";

const BrowsingInterface = ({
  frameDisplay,
  pickedFrames,
  setPickedFrames,
  loading = false,
  queryIndex,
  queryMode,
  searchType,
  teamPickedFrames,
  setTeamPickedFrames,
  browsingOption,
  setBrowsingOption,
  fetchTeamPickedFrames,
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const handleToggleSubmitConfirm = () => {
    setIsSubmitting(!isSubmitting);
  };
  const { handleDeleteTeamPickedFrameByIndex } = useHomeContext();
  const NOTIFICATION_DURATION = 3000;

  const [currentFrameIndex, setCurrentFrameIndex] = useState(null);
  const [playVideo, setPlayVideo] = useState(false);

  const initialVideoInfor = { path: "", startTime: 0 };
  const [videoInfor, setVideoInfor] = useState(initialVideoInfor);
  // const [browsingOption, setBrowsingOption] = useState("browsing");
  const [isFirstRender, setIsFirstRender] = useState(true);

  const [adjacentFrameInfo, setAdjacentFrameInfo] = useState({});
  const [isOpenAdjacentFrame, setIsOpenAdjacentFrame] = useState(false);
  const [listAdjacentFrames, setListAdjacentFrames] = useState([]);
  const [isSubmitConfirming, setIsSubmitConfirming] = useState(false);
  const initialSubmitFrame = {
    frame_number: 0,
    video_name: "",
    answer: "",
  };
  const [submitFrame, setSubmitFrame] = useState(initialSubmitFrame);
  const handleConfirmSubmit = () => {
    setIsSubmitConfirming(true);
  };

  const [isUploadConfirming, setIsUploadConfirming] = useState(false);

  const handleConfirmUpload = () => {
    setIsUploadConfirming(true);
  };
  const frameBrowsingAreaRef = useRef(null);

  const handleClickFrameItem = (event, frame, answer) => {
    event.stopPropagation();
    handlePickSubmitFrame(event, frame, answer);
    setPickedFrames([frame]);
  };

  const clearPickedFrames = () => {
    setPickedFrames([]);
  };

  const handlePickSingleFrame = (event, frame) => {
    event.stopPropagation();
    event.preventDefault();
    setPickedFrames([frame]);
  };
  // Không xài nữa
  const handlePickFrameItem = (event, frame) => {
    event.stopPropagation();
    event.preventDefault();
    setPickedFrames((prevPickedFrames) => {
      const newPickedFrames = prevPickedFrames.filter(
        (pickedFrame) => pickedFrame.id !== frame.id
      );

      // Kiểm tra xem có phần tử nào trong pickedFrames có trường answer hay không
      const existingFrameWithAnswer = prevPickedFrames.find(
        (pickedFrame) => pickedFrame.answer
      );

      // Nếu frame chưa tồn tại, thêm nó với thuộc tính mode và answer nếu có
      if (newPickedFrames.length === prevPickedFrames.length) {
        let frameToAdd = { ...frame, mode: queryMode }; // Thêm thuộc tính mode

        // Nếu đã có phần tử có answer, thêm answer đó vào frame mới
        if (existingFrameWithAnswer) {
          frameToAdd = {
            ...frameToAdd,
            answer: existingFrameWithAnswer.answer, // Thêm answer từ frame đã có
          };
        }

        newPickedFrames.push(frameToAdd);
      }

      return newPickedFrames;
    });
  };

  const handleDoubleClickFrameItem = async (frame) => {
    try {
      // const frame_infor = frameDisplay[index];
      const video_res = await get_video_by_name(frame.video_name);
      if (video_res && video_res.status >= 200 && video_res.status < 300) {
        const fps = video_res.data.fps;
        console.log("FPS VIDEO: ", fps);
        const duration = frame.frame_number / fps;
        setVideoInfor((prevData) => ({
          ...prevData,
          path: video_res.data.path,
          startTime: duration,
        }));
        setPlayVideo(true);
      } else {
        console.error("Error fetching video");
        setVideoInfor(initialVideoInfor);
      }
    } catch (error) {
      console.error("Get video failed:", error);
      setVideoInfor(initialVideoInfor);
    }
  };

  const handleClosePlayerVideo = () => {
    setPlayVideo(false);
  };

  const handleDisplayAdjacentFrame = async (event, frame) => {
    event.stopPropagation();
    setAdjacentFrameInfo(frame);

    const adjacentFrames = await get_adjacent_frame(
      frame.video_name,
      frame.frame_number
    );
    if (
      adjacentFrames &&
      adjacentFrames.status >= 200 &&
      adjacentFrames.status < 300
    ) {
      console.log(adjacentFrames);
      setIsOpenAdjacentFrame(true);
      console.log("adjacent frames: ", adjacentFrames.data.frames);
      setListAdjacentFrames(adjacentFrames.data.frames);
    }
  };

  function convertToTeamPickedFrames(pickedFrames) {
    // if (queryMode === "QA") {
    //   // Kiểm tra nếu bất kỳ frame nào thiếu answer
    //   for (let frame of pickedFrames) {
    //     if (!frame.answer || frame.answer.trim() === "") {
    //       NotificationManager.error(
    //         `Frame ${frame.frame_number} phải bao gồm answer`,
    //         "UPLOAD ERROR",
    //         NOTIFICATION_DURATION
    //       );
    //       return null; // Dừng việc upload
    //     }
    //   }
    // }

    return pickedFrames.map((frame, index) => {
      return {
        video_name: frame.video_name,
        frame_number: frame.frame_number, // Convert frame_number to string
        query_index: queryIndex,
        mode: queryMode,
        answer: queryMode === "TEXT" ? "" : QAAnswer, // Trường answer sẽ rỗng nếu queryMode là TEXT
      };
    });
  }

  const handleUploadPickedFrameToTeam = async () => {
    const uploadFrames = convertToTeamPickedFrames(pickedFrames);

    if (!uploadFrames) {
      // Nếu uploadFrames là null (có lỗi từ convertToTeamPickedFrames)
      return;
    }

    const res = await postTeamPickedFrames(uploadFrames);
    if (res && res.status >= 200 && res.status < 300) {
      console.log("upload res: ", res.data);
      if (res.data.team_picked.length > 0) {
        NotificationManager.success(
          "Upload successfully",
          "UPLOAD",
          NOTIFICATION_DURATION
        );
      } else {
        NotificationManager.success(
          "Nothing change",
          "UPLOAD",
          NOTIFICATION_DURATION
        );
      }
    } else {
      NotificationManager.error(
        "Upload failed",
        "UPLOAD",
        NOTIFICATION_DURATION
      );
    }
    setIsUploadConfirming(false);
  };

  // useEffect chỉ chạy khi pickedFrames thay đổi và không phải lần render đầu tiên
  useEffect(() => {
    if (isFirstRender) {
      setIsFirstRender(false);
      return;
    }
  }, [pickedFrames, isFirstRender]);

  useEffect(() => {
    console.log("team picked frame: ", teamPickedFrames);
  }, [teamPickedFrames]);

  const handlePickSubmitFrame = (event, frame, answer = "") => {
    // event.preventDefault();
    event.stopPropagation();
    setSubmitFrame((prevSubmitFrame) => {
      const prev = prevSubmitFrame;
      if (prev && prev.video_name === frame.frame_number && prev.video_name) {
        return initialSubmitFrame;
      } else {
        return { ...frame, answer: answer };
      }
    });
  };

  useEffect(() => {
    console.log("submit frame: ", submitFrame);
  }, [submitFrame]);
  // useEffect(() => {
  //   setPickedFrames([]);
  // }, [queryMode, queryIndex]);
  // useEffect(() => {
  //   const smFrame = submitFrame ? submitFrame.id : submitFrame;
  //   console.log("submitFrame:", smFrame);
  // }, [submitFrame]);

  const handleToggleQAAnswer = () => {
    setIsEnterQAAnswer(!isEnterQAAnswer);
  };
  const [isEnterQAAnswer, setIsEnterQAAnswer] = useState(false);

  const [QAAnswer, setQAAnswer] = useState("");
  const handleChangeQAAnswer = (event) => {
    setQAAnswer(event.target.value);
  };
  useEffect(() => {
    setSubmitFrame(initialSubmitFrame);
  }, []);

  const getFps = async (video_name) => {
    try {
      // const frame_infor = frameDisplay[index];
      const video_res = await get_video_by_name(video_name);
      if (video_res && video_res.status >= 200 && video_res.status < 300) {
        const fps = video_res.data.fps;
        return fps;
      } else {
        console.error("Error fetching video");
        return null;
      }
    } catch (error) {
      console.error("Get video failed:", error);
      return null;
    }
  };
  const submitQuery = async () => {
    const fps = await getFps(submitFrame.video_name);

    try {
      const submitResponse = await submit(
        queryMode,
        submitFrame.video_name,
        submitFrame.frame_number,
        fps,
        submitFrame.answer
      );
      console.log("submit response: ", submitResponse);
      NotificationManager.success(
        "SUBMIT THÀNH CÔNG",
        "SUBMIT",
        NOTIFICATION_DURATION
      );
    } catch (error) {
      console.error("Error submitting response: ", error);
      NotificationManager.error(
        `KHÔNG THỂ SUBMIT`,
        "SUBMIT",
        NOTIFICATION_DURATION
      );
    }
  };
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
    <div className="browsing-interface">
      <NotificationContainer />

      {isUploadConfirming && (
        <div className="submit-confirm">
          <div className="overlay"></div>
          <div className="confirm-popup">
            <div className="confirm-popup__header">
              <p>Confirm</p>
              <span
                className="close-button"
                onClick={() => {
                  setIsUploadConfirming(false);
                }}
              >
                &times;
              </span>
            </div>
            <div className="confirm-popup__content">
              Please confirm the current query index is
              <span className="query-index">{queryIndex}</span>!
            </div>
            <div className="confirm-popup__buttons">
              <button
                className="confirm-button confirm-button--no"
                onClick={() => {
                  setIsUploadConfirming(false);
                }}
              >
                CLOSE
              </button>

              <button
                className="confirm-button confirm-button--yes"
                onClick={handleUploadPickedFrameToTeam}
              >
                UPLOAD
              </button>
            </div>
          </div>
        </div>
      )}

      {isSubmitting && (
        <SubmitConfirm
          handleToggleSubmitConfirm={handleToggleSubmitConfirm}
          submitFrame={submitFrame}
          setSubmitFrame={setSubmitFrame}
          queryMode={queryMode}
        />
      )}
      <div className="browsing-option">
        <button
          className={`browsing-frames-btn ${
            browsingOption === "browsing" ? "activeBrwosingOption" : ""
          }`}
          onClick={() => setBrowsingOption("browsing")}
        >
          BROWSING FRAME
        </button>

        {/* <button
          className={`browsing-frames-btn ${
            browsingOption === "picked" ? "activeBrwosingOption" : ""
          }`}
          onClick={() => setBrowsingOption("picked")}
        >
          PICKED FRAMES
        </button> */}
        <button
          className={`browsing-frames-btn team-picked-btn ${
            browsingOption === "team-picked" ? "activeBrwosingOption" : ""
          }`}
          onClick={() => setBrowsingOption("team-picked")}
        >
          TEAM PICKED
        </button>
        <div className="submit-services">
          <button
            className="submit-btn"
            type="button"
            onClick={(event) => {
              event.stopPropagation();
              handleToggleSubmitConfirm();
            }}
          >
            Submit
          </button>
          {browsingOption === "team-picked" && (
            <>
              <button
                type="button"
                className="reload-picked-frames"
                onClick={fetchTeamPickedFrames}
                // onClick={handleConfirmUpload}
              >
                <svg
                  // fill="#000000"
                  fill="none"
                  stroke="#000000"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g
                    id="SVGRepo_tracerCarrier"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></g>
                  <g id="SVGRepo_iconCarrier">
                    <path d="M4,12a1,1,0,0,1-2,0A9.983,9.983,0,0,1,18.242,4.206V2.758a1,1,0,1,1,2,0v4a1,1,0,0,1-1,1h-4a1,1,0,0,1,0-2h1.743A7.986,7.986,0,0,0,4,12Zm17-1a1,1,0,0,0-1,1A7.986,7.986,0,0,1,7.015,18.242H8.757a1,1,0,1,0,0-2h-4a1,1,0,0,0-1,1v4a1,1,0,0,0,2,0V19.794A9.984,9.984,0,0,0,22,12,1,1,0,0,0,21,11Z"></path>
                  </g>
                </svg>
              </button>
              {/* <button
                type="button"
                className="submit-frames-btn"
                onClick={handleConfirmSubmit}
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g
                    id="SVGRepo_tracerCarrier"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></g>
                  <g id="SVGRepo_iconCarrier">
                    {" "}
                    <path
                      d="M12.5 4V17M12.5 17L7 12.2105M12.5 17L18 12.2105"
                      stroke="#000000"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    ></path>{" "}
                    <path
                      d="M6 21H19"
                      stroke="#000000"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    ></path>{" "}
                  </g>
                </svg>
              </button> */}
              <button
                type="button"
                className="clear-picked-frames-btn"
                onClick={(event) => {
                  handleDeleteTeamPickedFrameByIndex(event, queryIndex);
                }}
              >
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g
                    id="SVGRepo_tracerCarrier"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></g>
                  <g id="SVGRepo_iconCarrier">
                    {" "}
                    <path
                      d="M6 7V18C6 19.1046 6.89543 20 8 20H16C17.1046 20 18 19.1046 18 18V7M6 7H5M6 7H8M18 7H19M18 7H16M10 11V16M14 11V16M8 7V5C8 3.89543 8.89543 3 10 3H14C15.1046 3 16 3.89543 16 5V7M8 7H16"
                      stroke="#000000"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    ></path>{" "}
                  </g>
                </svg>
              </button>
            </>
          )}

          {browsingOption !== "team-picked" && (
            <button
              type="button"
              className="upload-picked-frames"
              // onClick={handleConfirmUpload}
              onClick={handleUploadPickedFrameToTeam}
            >
              <svg
                viewBox="0 0 1024 1024"
                class="icon"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                fill="#000000"
              >
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                <g
                  id="SVGRepo_tracerCarrier"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                ></g>
                <g id="SVGRepo_iconCarrier">
                  <path
                    d="M736.68 435.86a173.773 173.773 0 0 1 172.042 172.038c0.578 44.907-18.093 87.822-48.461 119.698-32.761 34.387-76.991 51.744-123.581 52.343-68.202 0.876-68.284 106.718 0 105.841 152.654-1.964 275.918-125.229 277.883-277.883 1.964-152.664-128.188-275.956-277.883-277.879-68.284-0.878-68.202 104.965 0 105.842zM285.262 779.307A173.773 173.773 0 0 1 113.22 607.266c-0.577-44.909 18.09-87.823 48.461-119.705 32.759-34.386 76.988-51.737 123.58-52.337 68.2-0.877 68.284-106.721 0-105.842C132.605 331.344 9.341 454.607 7.379 607.266 5.417 759.929 135.565 883.225 285.262 885.148c68.284 0.876 68.2-104.965 0-105.841z"
                    fill="#4A5699"
                  ></path>
                  <path
                    d="M339.68 384.204a173.762 173.762 0 0 1 172.037-172.038c44.908-0.577 87.822 18.092 119.698 48.462 34.388 32.759 51.743 76.985 52.343 123.576 0.877 68.199 106.72 68.284 105.843 0-1.964-152.653-125.231-275.917-277.884-277.879-152.664-1.962-275.954 128.182-277.878 277.879-0.88 68.284 104.964 68.199 105.841 0z"
                    fill="#C45FA0"
                  ></path>
                  <path
                    d="M545.039 473.078c16.542 16.542 16.542 43.356 0 59.896l-122.89 122.895c-16.542 16.538-43.357 16.538-59.896 0-16.542-16.546-16.542-43.362 0-59.899l122.892-122.892c16.537-16.542 43.355-16.542 59.894 0z"
                    fill="#F39A2B"
                  ></path>
                  <path
                    d="M485.17 473.078c16.537-16.539 43.354-16.539 59.892 0l122.896 122.896c16.538 16.533 16.538 43.354 0 59.896-16.541 16.538-43.361 16.538-59.898 0L485.17 532.979c-16.547-16.543-16.547-43.359 0-59.901z"
                    fill="#F39A2B"
                  ></path>
                  <path
                    d="M514.045 634.097c23.972 0 43.402 19.433 43.402 43.399v178.086c0 23.968-19.432 43.398-43.402 43.398-23.964 0-43.396-19.432-43.396-43.398V677.496c0.001-23.968 19.433-43.399 43.396-43.399z"
                    fill="#E5594F"
                  ></path>
                </g>
              </svg>
            </button>
          )}
          {/* {browsingOption !== "team-picked" && (
            <button
              type="button"
              className="clear-picked-frames-btn"
              onClick={clearPickedFrames}
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                <g
                  id="SVGRepo_tracerCarrier"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                ></g>
                <g id="SVGRepo_iconCarrier">
                  {" "}
                  <path
                    d="M6 7V18C6 19.1046 6.89543 20 8 20H16C17.1046 20 18 19.1046 18 18V7M6 7H5M6 7H8M18 7H19M18 7H16M10 11V16M14 11V16M8 7V5C8 3.89543 8.89543 3 10 3H14C15.1046 3 16 3.89543 16 5V7M8 7H16"
                    stroke="#000000"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></path>{" "}
                </g>
              </svg>
            </button>
          )} */}
        </div>
      </div>
      <span className="cus-divider"></span>
      {browsingOption === "browsing" && (
        <ul className="frame-browsing-area" ref={frameBrowsingAreaRef}>
          {frameDisplay &&
            searchType === "ARRAY" &&
            frameDisplay.map((frame, index) => (
              <li
                key={index}
                className={`frame-item ${
                  submitFrame &&
                  submitFrame.frame_number === frame.frame_number &&
                  submitFrame.video_name === frame.video_name
                    ? "frame-item-selected"
                    : ""
                }`}
                onClick={(event) => {
                  event.stopPropagation();
                  handleClickFrameItem(event, frame, QAAnswer);
                  handlePickSingleFrame(event, frame, QAAnswer);
                }}
                onDoubleClick={() => handleDoubleClickFrameItem(frame)}
              >
                <img
                  src={`${process.env.REACT_APP_LOCAL_ENDPOINT_FRAMES}/${frame.video_name}/${frame.frame_number}.jpg`}
                  onError={(e) => {
                    e.target.onerror = null; // Ngăn sự kiện lặp lại để tránh vòng lặp
                    e.target.src = `${process.env.REACT_APP_DEFAULT_ENDPOINT_FRAMES}/${frame.video_name}/${frame.frame_number}.jpg`; // Thay thế bằng ảnh mặc định
                  }}
                  alt="img-frame"
                  className="img-frame"
                />
                {/* <input
                  type="checkbox"
                  name={`frame-item-check-${index}`}
                  className="frame-item-checkbox"
                  checked={pickedFrames.some(
                    (pickedFrame) => pickedFrame.id === frame.id
                  )}
                  onChange={(event) => {
                    event.stopPropagation();
                    handlePickFrameItem(event, frame);
                  }}
                />
                <div
                  className="cus-checkbox"
                  name={`frame-item-cus-check-${index}`}
                ></div> */}

                <div className="metadata">
                  <span className="metadata_video-name">
                    {frame.video_name}
                  </span>
                  <span className="metadata_frame-number">
                    {frame.frame_number}
                  </span>
                </div>
                <div className="frame-service">
                  <button
                    type="button"
                    className="display-adjacent-frame-btn"
                    onClick={(event) => {
                      handleDisplayAdjacentFrame(event, frame);
                    }}
                  >
                    Adjacent
                  </button>
                  {queryMode === "QA" && (
                    <button
                      type="button"
                      className="enter-answer-button"
                      onClick={(event) => {
                        // handleDisplayAdjacentFrame(event, frame);
                        handleClickFrameItem(event, frame, QAAnswer);
                        handleToggleQAAnswer();
                      }}
                    >
                      Answer
                    </button>
                  )}
                  <div
                    className={
                      submitFrame &&
                      submitFrame.frame_number === frame.frame_number &&
                      submitFrame.video_name === frame.video_name
                        ? "cus-submit-checkbox--active"
                        : "cus-submit-checkbox"
                    }
                    onClick={(event) => {
                      event.stopPropagation();
                      handlePickSubmitFrame(event, frame);
                    }}
                    name={`pick-submit-${index}`}
                  ></div>
                </div>
              </li>
            ))}
          {frameDisplay &&
            searchType === "GRID" &&
            frameDisplay.map((arrayFrames, indexVideo) => (
              <div className="frame-display-row">
                {arrayFrames.map((frame, index) => (
                  <li
                    key={index}
                    className={`frame-item ${
                      submitFrame &&
                      submitFrame.frame_number === frame.frame_number &&
                      submitFrame.video_name === frame.video_name
                        ? "frame-item-selected"
                        : ""
                    }`}
                    onClick={(event) => {
                      event.stopPropagation();
                      handleClickFrameItem(event, frame, QAAnswer);
                      handlePickSingleFrame(event, frame, QAAnswer);
                    }}
                    onDoubleClick={() => handleDoubleClickFrameItem(frame)}
                  >
                    <img
                      src={`${process.env.REACT_APP_LOCAL_ENDPOINT_FRAMES}/${frame.video_name}/${frame.frame_number}.jpg`}
                      onError={(e) => {
                        e.target.onerror = null; // Ngăn sự kiện lặp lại để tránh vòng lặp
                        e.target.src = `${process.env.REACT_APP_DEFAULT_ENDPOINT_FRAMES}/${frame.video_name}/${frame.frame_number}.jpg`; // Thay thế bằng ảnh mặc định
                      }}
                      alt="img-frame"
                      className="img-frame"
                    />
                    {/* <input
                  type="checkbox"
                  name={`frame-item-check-${index}`}
                  className="frame-item-checkbox"
                  checked={pickedFrames.some(
                    (pickedFrame) => pickedFrame.id === frame.id
                  )}
                  onChange={(event) => {
                    event.stopPropagation();
                    handlePickFrameItem(event, frame);
                  }}
                />
                <div
                  className="cus-checkbox"
                  name={`frame-item-cus-check-${index}`}
                ></div> */}

                    <div className="metadata">
                      <span className="metadata_video-name">
                        {frame.video_name}
                      </span>
                      <span className="metadata_frame-number">
                        {frame.frame_number}
                      </span>
                    </div>
                    <div className="frame-service">
                      <button
                        type="button"
                        className="display-adjacent-frame-btn"
                        onClick={(event) => {
                          handleDisplayAdjacentFrame(event, frame);
                        }}
                      >
                        Adjacent
                      </button>
                      {queryMode === "QA" && (
                        <button
                          type="button"
                          className="enter-answer-button"
                          onClick={(event) => {
                            // handleDisplayAdjacentFrame(event, frame);
                            handleToggleQAAnswer();
                            handleClickFrameItem(event, frame, QAAnswer);
                          }}
                        >
                          Answer
                        </button>
                      )}
                      <div
                        className={
                          submitFrame &&
                          submitFrame.frame_number === frame.frame_number &&
                          submitFrame.video_name === frame.video_name
                            ? "cus-submit-checkbox--active"
                            : "cus-submit-checkbox"
                        }
                        onClick={(event) => {
                          event.stopPropagation();
                          handlePickSubmitFrame(event, frame);
                        }}
                        name={`pick-submit-${index}`}
                      ></div>
                    </div>
                  </li>
                ))}
              </div>
            ))}
        </ul>
      )}

      {browsingOption === "picked" && (
        <PickedFrames
          setPickedFrames={setPickedFrames}
          pickedFrames={pickedFrames}
          framesDisplay={frameDisplay}
          currentFrameIndex={currentFrameIndex}
          setCurrentFrameIndex={setCurrentFrameIndex}
          handleClickFrameItem={handleClickFrameItem}
          handleDoubleClickFrameItem={handleDoubleClickFrameItem}
          handlePickFrameItem={handlePickFrameItem}
          handleDisplayAdjacentFrame={handleDisplayAdjacentFrame}
          queryIndex={queryIndex}
          queryMode={queryMode}
        />
      )}
      {isEnterQAAnswer && (
        <QAInput
          handleChangeQAAnswer={handleChangeQAAnswer}
          queryIndex={queryIndex}
          handleToggleQAAnswer={handleToggleQAAnswer}
          QAAnswer={QAAnswer}
          setQAAnswer={setQAAnswer}
          // handleUploadAnswer={handleUpdateAnswer}
          currentFrame={submitFrame}
          oldAnswer={submitFrame.answer || ""}
        />
      )}
      {browsingOption === "team-picked" && (
        <TeamPickedFrames
          isSubmitConfirming={isSubmitConfirming}
          setIsSubmitConfirming={setIsSubmitConfirming}
          queryIndex={queryIndex}
          teamPickedFrames={teamPickedFrames}
          setTeamPickedFrames={setTeamPickedFrames}
          fetchTeamPickedFrames={fetchTeamPickedFrames}
          queryMode={queryMode}
          submitFrame={submitFrame}
          setSubmitFrame={setSubmitFrame}
          initialSubmitFrame={initialSubmitFrame}
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
      )}
      {isOpenAdjacentFrame && (
        <AdjacentFrame
          listAdjacentFrame={listAdjacentFrames}
          middleFrame={adjacentFrameInfo}
          setIsOpenAdjacentFrame={setIsOpenAdjacentFrame}
          handlePickFrameItem={handlePickFrameItem}
          pickedFrames={pickedFrames}
          setPickedFrames={setPickedFrames}
          setIsUploadConfirming={setIsUploadConfirming}
        />
      )}
    </div>
  );
};

export default BrowsingInterface;

import React, { useState, useEffect } from "react";
import "./TeamPickedFrames.scss";
import submitFrames from "../../services/submit_frames";
import getTeamPickedFrames from "../../services/get_team_picked";
import { NotificationManager } from "react-notifications";
import updateTeamPickedFrame from "../../services/update_team_picked_frame";
import { ReactSortable } from "react-sortablejs";
import deleteTeamPickedFrame from "../../services/delete_team_picked_frame";
import QAInput from "../QAInput/QAInput";
import updateQAAnswer from "../../services/update_qa";
import AdjacentFrame from "../AdjacentFrame/AdjacentFrame";
import get_adjacent_frame from "../../services/get_adjacent_frame";
import postTeamPickedFrames from "../../services/upload_to_team_picked";
import get_video from "../../services/get_video";
import get_video_by_name from "../../services/get_video_by_name";
import VideoPlayer from "../VideoPlayer/VideoPlayer";
const TeamPickedFrames = ({
  isSubmitConfirming,
  setIsSubmitConfirming,
  queryIndex,
  teamPickedFrames,
  setTeamPickedFrames,
  fetchTeamPickedFrames,
  queryMode,
  submitFrame,
  setSubmitFrame,
  initialSubmitFrame,
}) => {
  const [pickedFrames, setPickedFrames] = useState([]);
  const NOTIFICATION_DURATION = 2000;
  const [QAAnswer, setQAAnswer] = useState("");
  const [isEnterQAAnswer, setIsEnterQAAnswer] = useState(false);
  const [currentFrame, setCurrentFrame] = useState(null);

  const handleChangeQAAnswer = (event) => {
    setQAAnswer(event.target.value);
  };

  const handleToggleQAAnswer = () => {
    setIsEnterQAAnswer(!isEnterQAAnswer);
  };
  const confirmSubmit = async () => {
    if (teamPickedFrames.length > 0) {
      const response = await submitFrames(
        teamPickedFrames,
        queryMode,
        queryIndex
      );
      if (response.status === 200) {
        setIsSubmitConfirming(false);
        NotificationManager.success("Submit successfully", "SUBMIT", 3000);
      } else {
        NotificationManager.error("Submit failed", "SUBMIT", 3000);
      }
    }
  };
  function convertToTeamPickedFrames(teamPickedFrames, pickedFrames) {
    const existingAnswer = teamPickedFrames.find(
      (frame) => frame.answer
    )?.answer;

    return pickedFrames.map((frame, index) => {
      return {
        video_name: frame.video_name,
        frame_number: frame.frame_number, // Convert frame_number to string
        query_index: queryIndex,
        mode: queryMode,
        path: frame.path,
        answer: existingAnswer || "", // Trường answer sẽ rỗng nếu queryMode là TEXT
        duration: frame.duration,
      };
    });
  }

  const handleEnd = async (newList) => {
    // Kiểm tra xem danh sách có thực sự thay đổi hay không
    const hasChanged =
      JSON.stringify(newList) !== JSON.stringify(teamPickedFrames);
    if (hasChanged) {
      setTeamPickedFrames(newList);
      const response = await updateTeamPickedFrame(newList);
      if (response && response.status >= 200 && response.status < 300) {
        // Update team_picked_frames
        console.log("UPDATE TEAM PICKED SUCCESS!");
        NotificationManager.success("Update successfully", "UPDATE", 3000);
      }
    }
  };

  const handleDeleteTeamPickedFrame = async (event, frame) => {
    event.preventDefault();
    const response = await deleteTeamPickedFrame(frame.id);
    if (response && response.status >= 200 && response.status < 300) {
      // Update team_picked_frames
      console.log("DELETE TEAM PICKED FRAME SUCCESS!");
      NotificationManager.success("Delete successfully", "DELETE", 3000);
      // Update team_picked_frames
      fetchTeamPickedFrames();
    }
  };

  const handleUpdateAnswer = async () => {
    // Update answer
    const res = await updateQAAnswer(currentFrame.id, QAAnswer);
    if (res && res.status >= 200 && res.status < 300) {
      console.log("UPDATE ANSWER SUCCESS!");
      NotificationManager.success("Update answer successfully", "UPDATE", 3000);
      // Update team_picked_frames
      fetchTeamPickedFrames();
    } else {
      console.log("UPDATE ANSWER FAIL!");
      NotificationManager.error("Update answer failed", "UPDATE", 3000);
    }
  };
  useEffect(() => {
    fetchTeamPickedFrames();
  }, [queryIndex, queryMode]);

  const [adjacentFrameInfo, setAdjacentFrameInfo] = useState({});
  const [isOpenAdjacentFrame, setIsOpenAdjacentFrame] = useState(false);
  const [listAdjacentFrames, setListAdjacentFrames] = useState([]);
  // const [frameToAdd, setFrameToAdd] = useState([]);
  const handleAddFramesToTeamPicked = async (event, frames) => {
    event.stopPropagation();
    // const framesToAdd = [frame];
    const uploadFrames = convertToTeamPickedFrames(teamPickedFrames, frames);

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
        fetchTeamPickedFrames();
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

  const [playVideo, setPlayVideo] = useState(false);
  const initialVideoInfor = { path: "", startTime: 0 };
  const [videoInfor, setVideoInfor] = useState(initialVideoInfor);
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

  const handlePickSubmitFrame = (event, frame, answer = "") => {
    // event.preventDefault();
    event.stopPropagation();
    setSubmitFrame((prevSubmitFrame) => {
      const prev = prevSubmitFrame;
      if (prev && prev.id === frame.id) {
        return initialSubmitFrame;
      } else {
        return { ...frame, answer: answer };
      }
    });
  };
  return (
    <div className="team-picked-frames frame-browsing-area">
      {/* <NotificationContainer /> */}
      {isOpenAdjacentFrame && (
        <AdjacentFrame
          page="teamPickedFrames"
          listAdjacentFrame={listAdjacentFrames}
          middleFrame={adjacentFrameInfo}
          setIsOpenAdjacentFrame={setIsOpenAdjacentFrame}
          // handlePickFrameItem={handleAddFrameToTeamPicked}
          setPickedFrames={setPickedFrames}
          pickedFrames={pickedFrames}
          uploadToTeamPickedFrames={handleAddFramesToTeamPicked}
        />
      )}
      {isEnterQAAnswer && (
        <QAInput
          handleChangeQAAnswer={handleChangeQAAnswer}
          queryIndex={queryIndex}
          handleToggleQAAnswer={handleToggleQAAnswer}
          QAAnswer={QAAnswer}
          setQAAnswer={setQAAnswer}
          handleUploadAnswer={handleUpdateAnswer}
          currentFrame={currentFrame}
          oldAnswer={currentFrame.answer || ""}
          type="team"
        />
      )}
      {isSubmitConfirming && (
        <div className="submit-confirm">
          <div className="overlay"></div>
          <div className="confirm-popup">
            <div className="confirm-popup__header">
              <p>Confirm</p>
              <span
                className="close-button"
                onClick={() => {
                  setIsSubmitConfirming(false);
                }}
              >
                &times;
              </span>
            </div>
            <div className="confirm-popup__content">
              Submit answer to query index{" "}
              <span className="query-index">{queryIndex}</span>?
            </div>
            <div className="confirm-popup__buttons">
              <button
                className="confirm-button confirm-button--no"
                onClick={() => {
                  setIsSubmitConfirming(false);
                }}
              >
                CLOSE
              </button>

              <button
                className="confirm-button confirm-button--yes"
                // onClick={confirmSubmit}
                onClick={() => {
                  confirmSubmit(teamPickedFrames);
                }}
              >
                SUBMIT
              </button>
            </div>
          </div>
        </div>
      )}
      <ReactSortable
        list={teamPickedFrames}
        setList={(newList) => {
          handleEnd(newList);
        }}
        animation={200}
        delayOnTouchStart={true}
        delay={2}
        swapThreshold={0.65}
        className="picked-frames-container frame-browsing-area"
      >
        {/* <ul className="picked-frames-container frame-browsing-area"> */}
        {/* NotificationManager.success('Success message', 'Title here'); */}
        {teamPickedFrames.map((frame, index) => (
          <li
            className={`frame-item ${
              submitFrame && submitFrame.id === frame.id
                ? "frame-item-selected"
                : null
            }`}
            onDoubleClick={() => handleDoubleClickFrameItem(frame)}
            onClick={(event) =>
              handlePickSubmitFrame(event, frame, frame.answer)
            }
          >
            <img
              src={`${process.env.REACT_APP_LOCAL_ENDPOINT_FRAMES}/${frame.video_name}/${frame.frame_number}.jpg`}
              alt="img-frame"
              className="img-frame"
              onError={(e) => {
                e.target.onerror = null; // Ngăn sự kiện lặp lại để tránh vòng lặp
                e.target.src = `${process.env.REACT_APP_DEFAULT_ENDPOINT_FRAMES}/${frame.video_name}/${frame.frame_number}.jpg`; // Thay thế bằng ảnh mặc định
              }}
            />
            {/* <input
              type="checkbox"
              name={`frame-item-check-${index}`}
              className="frame-item-checkbox"
              checked={teamPickedFrames.some(
                (teamPickedFrame) => teamPickedFrame.id === frame.id
              )}
              onChange={(event) => handleDeleteTeamPickedFrame(event, frame)}
            />
            <div
              className="cus-checkbox"
              name={`frame-item-cus-check-${frame}`}
            ></div> */}
            <div className="metadata">
              <span className="metadata_video-name">{frame.video_name}</span>
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
                    setCurrentFrame(frame);
                  }}
                >
                  Answer
                </button>
              )}
            </div>
            <div
              className={
                submitFrame && submitFrame.id === frame.id
                  ? "cus-submit-checkbox--active"
                  : "cus-submit-checkbox"
              }
              onClick={(event) => {
                event.stopPropagation();
                handlePickSubmitFrame(event, frame);
              }}
              name={`pick-submit-${index}`}
            ></div>
          </li>
        ))}
        {/* </ul> */}
      </ReactSortable>
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
    </div>
  );
};

export default TeamPickedFrames;

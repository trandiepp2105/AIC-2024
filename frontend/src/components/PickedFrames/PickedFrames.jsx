import React, { useEffect, useState } from "react";
import "./PickedFrames.scss";
import { ReactSortable } from "react-sortablejs";
import postTeamPickedFrames from "../../services/upload_to_team_picked";
import QAInput from "../QAInput/QAInput";
import { NotificationManager } from "react-notifications";
const PickedFrames = ({
  pickedFrames,
  setPickedFrames,
  currentFrameIndex,
  handleClickFrameItem,
  handleDoubleClickFrameItem,
  handlePickFrameItem,
  handleDisplayAdjacentFrame,
  queryIndex,
  queryMode,
}) => {
  // useEffect(() => {
  //   console.log("picked frames: ", pickedFrames);
  // }, [pickedFrames]);
  // Hàm để xử lý khi kéo-thả kết thúc
  const onDragEnd = () => {
    console.log("picked frame: ", pickedFrames);
  };

  const [QAAnswer, setQAAnswer] = useState("");
  const [isEnterQAAnswer, setIsEnterQAAnswer] = useState(false);
  const handleChangeQAAnswer = (event) => {
    setQAAnswer(event.target.value);
  };

  const handleToggleQAAnswer = () => {
    setIsEnterQAAnswer(!isEnterQAAnswer);
  };

  const handleUploadAnswer = (answer, frameId) => {
    if (!answer) {
      NotificationManager.error("Please enter answer!", "ANSWER", 3000);
      return false;
    }

    // Kiểm tra nếu toàn bộ pickedFrames đều chưa có trường answer
    const isAllFramesWithoutAnswer = pickedFrames.every(
      (frame) => !frame.answer
    );

    setPickedFrames((prevPickedFrames) => {
      return prevPickedFrames.map((frame) => {
        // Nếu tất cả các frame đều chưa có answer, thì thêm answer cho tất cả
        if (isAllFramesWithoutAnswer) {
          NotificationManager.success(
            "Added answer to all frames",
            "ANSWER",
            3000
          );
          return {
            ...frame,
            answer: answer, // Thêm trường answer vào tất cả frame
          };
        }

        // Nếu không thì chỉ thêm answer cho frame hiện tại
        if (frame.id === frameId) {
          NotificationManager.success("Enter answer success", "ANSWER", 3000);
          return {
            ...frame,
            answer: answer, // Thêm answer cho frame đang được xử lý
          };
        }

        return frame;
      });
    });

    return true;
  };

  const [currentFrame, setCurrentFrame] = useState(null);

  return (
    <>
      {isEnterQAAnswer && (
        <QAInput
          handleChangeQAAnswer={handleChangeQAAnswer}
          queryIndex={queryIndex}
          handleToggleQAAnswer={handleToggleQAAnswer}
          QAAnswer={QAAnswer}
          setQAAnswer={setQAAnswer}
          handleUploadAnswer={handleUploadAnswer}
          currentFrame={currentFrame}
          oldAnswer={currentFrame.answer || ""}
        />
      )}
      <ReactSortable
        list={pickedFrames}
        setList={setPickedFrames}
        animation={200}
        delayOnTouchStart={true}
        delay={2}
        swapThreshold={0.65}
        onEnd={onDragEnd}
        className="picked-frames-container frame-browsing-area"
      >
        {/* <ul className="picked-frames-container frame-browsing-area"> */}
        {/* NotificationManager.success('Success message', 'Title here'); */}
        {pickedFrames.map((frame, index) => (
          <li
            className={`frame-item ${
              currentFrameIndex === index ? "frame-item-selected" : ""
            } frame-item-group`}
            onClick={(event) => handleClickFrameItem(event, index)}
            onDoubleClick={() => handleDoubleClickFrameItem(frame)}
          >
            <img src={frame.path} alt="img-frame" className="img-frame" />
            <input
              type="checkbox"
              name={`frame-item-check-${index}`}
              className="frame-item-checkbox"
              checked={pickedFrames.some(
                (pickedFrame) => pickedFrame.id === frame.id
              )}
              onChange={(event) => handlePickFrameItem(event, frame)}
            />
            <div
              className="cus-checkbox"
              name={`frame-item-cus-check-${frame}`}
            ></div>
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
          </li>
        ))}
        {/* </ul> */}
      </ReactSortable>
    </>
  );
};

export default PickedFrames;

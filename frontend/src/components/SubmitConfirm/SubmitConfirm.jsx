import React, { useEffect, useRef } from "react";
import "./SubmitConfirm.scss";
import submit from "../../services/submit";
import submitFrameQuery from "../../services/submitFrameQuery";
import get_video_by_name from "../../services/get_video_by_name";
import {
  NotificationContainer,
  NotificationManager,
} from "react-notifications";
const SubmitConfirm = ({
  handleToggleSubmitConfirm,
  submitFrame,
  setSubmitFrame,
  queryMode,
}) => {
  const wrapperRef = useRef(null);
  const textAreaRef = useRef(null); // Tham chiếu tới textarea

  useEffect(() => {
    // Hàm kiểm tra nếu click ngoài vùng wrapper-qa-input
    const handleClickOutside = (event) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        handleToggleSubmitConfirm(); // Đóng cửa sổ nếu click bên ngoài
      }
    };

    // Thêm sự kiện click vào document
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      // Hủy sự kiện khi component bị unmount
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [handleToggleSubmitConfirm]);

  // Hàm xử lý sự kiện khi nhấn phím trong textarea
  const handleKeyDown = (event) => {
    console.log("onKeyDown");
    if (event.key === "Enter") {
      if (event.shiftKey) {
        // Cho phép xuống dòng khi nhấn Shift + Enter
        return;
      } else {
        // Ngăn hành vi mặc định của Enter (tạo dòng mới) và thực hiện upload câu trả lời
        event.preventDefault();
      }
    }
  };

  // useEffect(() => {
  //   setQAAnswer(oldAnswer || ""); // Thiết lập giá trị QAAnswer từ oldAnswer khi render lần đầu
  //   if (textAreaRef.current) {
  //     textAreaRef.current.focus(); // Focus vào textarea khi component render
  //     // Đặt con trỏ vào cuối đoạn văn bản
  //     textAreaRef.current.selectionStart = textAreaRef.current.selectionEnd =
  //       textAreaRef.current.value.length;
  //   }
  // }, [setQAAnswer, oldAnswer]);

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

  useEffect(() => {
    console.log("submit frame: ", submitFrame);
  });

  const handleChangeQAAnswer = (event) => {
    // Cập nhật giá trị answer của submitFrame
    setSubmitFrame((prevFrame) => ({
      ...prevFrame,
      answer: event.target.value,
    }));
  };

  const submitQuery = async () => {
    // const fps = await getFps(submitFrame);
    // const submitRes = submit(
    //   queryMode,
    //   submitFrame.video_name,
    //   submitFrame.frame_number,
    //   fps,
    //   submitFrame.answer
    // );
    // console.log("submitRes: ", submitRes);
    const submitRes = await submitFrameQuery(
      queryMode,
      submitFrame.video_name,
      submitFrame.frame_number,
      submitFrame.answer
    );

    if (submitRes && submitRes.submission === "CORRECT") {
      NotificationManager.success("SUBMIT SUCCESSFULL", "SUBMIT", 7000);
      handleToggleSubmitConfirm();
      return;
    }
    handleToggleSubmitConfirm();
    NotificationManager.error("SUBMIT FAILED", "SUBMIT", 7000);
  };
  return (
    <div className="qa-input">
      <div className="overlay"></div>
      <div className="display-frame-aswer">
        <img
          src={`${process.env.REACT_APP_LOCAL_ENDPOINT_FRAMES}/${submitFrame.video_name}/${submitFrame.frame_number}.jpg`}
          alt="adjacent-frame"
          onError={(e) => {
            e.target.onerror = null; // Ngăn sự kiện lặp lại để tránh vòng lặp
            e.target.src = `${process.env.REACT_APP_DEFAULT_ENDPOINT_FRAMES}/${submitFrame.video_name}/${submitFrame.frame_number}.jpg`; // Thay thế bằng ảnh mặc định
          }}
        />
        <div className="metadata">
          <div className="video-name">{submitFrame.video_name}</div>
          <div className="frame_number">{submitFrame.frame_number}</div>
        </div>
      </div>
      <div className="wrapper-qa-input" ref={wrapperRef}>
        <div className="title">
          SUBMIT AT FRAME
          <span className="special-title">
            {submitFrame.frame_number}
            {/* {" "}
            {submitFrame.frame_number || 0}{" "} */}
          </span>
          VIDEO
          <span className="special-title">
            {submitFrame.video_name}
            {/* {" "}
            
            {submitFrame.video_name || "NONE"} */}
          </span>
          !
        </div>
        <textarea
          name="qa-input-area"
          id=""
          className="qa-input-area"
          onInput={handleChangeQAAnswer}
          onKeyDown={handleKeyDown} // Gắn sự kiện khi nhấn phím
          ref={textAreaRef} // Tham chiếu tới textarea
          value={submitFrame.answer} // Gán giá trị QAAnswer vào textarea
        ></textarea>
        <div className="button-service">
          <button
            type="button"
            className="upload-button"
            // onClick={() => {
            //   if (type === "team") {
            //     const res = handleUploadAnswer(QAAnswer, currentFrame.id);
            //     if (res) {
            //       handleToggleSubmitConfirm();
            //     }
            //   } else {
            //     handleToggleSubmitConfirm();
            //   }
            // }}
            onClick={submitQuery}
          >
            SUBMIT
          </button>
          <button
            type="button"
            className="close-button"
            onClick={handleToggleSubmitConfirm}
          >
            CLOSE
          </button>
        </div>
      </div>
    </div>
  );
};

export default SubmitConfirm;

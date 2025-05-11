import React, { useEffect, useRef } from "react";
import "./QAInput.scss";

const QAInput = ({
  handleChangeQAAnswer,
  handleToggleQAAnswer,
  queryIndex,
  currentFrame,
  handleUploadAnswer,
  QAAnswer,
  setQAAnswer,
  oldAnswer,
  type = "browsing",
}) => {
  const wrapperRef = useRef(null);
  const textAreaRef = useRef(null); // Tham chiếu tới textarea

  useEffect(() => {
    // Hàm kiểm tra nếu click ngoài vùng wrapper-qa-input
    const handleClickOutside = (event) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        handleToggleQAAnswer(); // Đóng cửa sổ nếu click bên ngoài
      }
    };

    // Thêm sự kiện click vào document
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      // Hủy sự kiện khi component bị unmount
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [handleToggleQAAnswer]);

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
        if (type === "team") {
          const res = handleUploadAnswer(QAAnswer, currentFrame.id);
          if (res) {
            handleToggleQAAnswer();
          }
        } else {
          handleToggleQAAnswer();
        }
      }
    }
  };

  useEffect(() => {
    setQAAnswer(oldAnswer || ""); // Thiết lập giá trị QAAnswer từ oldAnswer khi render lần đầu
    if (textAreaRef.current) {
      textAreaRef.current.focus(); // Focus vào textarea khi component render
      // Đặt con trỏ vào cuối đoạn văn bản
      textAreaRef.current.selectionStart = textAreaRef.current.selectionEnd =
        textAreaRef.current.value.length;
    }
  }, [setQAAnswer, oldAnswer]);

  return (
    <div className="qa-input">
      <div className="overlay"></div>
      <div className="wrapper-qa-input" ref={wrapperRef}>
        <div className="title">
          ENTER ANSWER FOR
          <span className="special-title"> QUERY {queryIndex}</span> AT FRAME
          <span className="special-title"> {currentFrame.frame_number} </span>
          VIDEO
          <span className="special-title"> {currentFrame.video_name}</span>!
        </div>
        <textarea
          name="qa-input-area"
          id=""
          className="qa-input-area"
          onInput={handleChangeQAAnswer}
          onKeyDown={handleKeyDown} // Gắn sự kiện khi nhấn phím
          ref={textAreaRef} // Tham chiếu tới textarea
          value={QAAnswer} // Gán giá trị QAAnswer vào textarea
        ></textarea>
        <div className="button-service">
          <button
            type="button"
            className="upload-button"
            onClick={() => {
              if (type === "team") {
                const res = handleUploadAnswer(QAAnswer, currentFrame.id);
                if (res) {
                  handleToggleQAAnswer();
                }
              } else {
                handleToggleQAAnswer();
              }
            }}
          >
            ENTER
          </button>
          <button
            type="button"
            className="close-button"
            onClick={handleToggleQAAnswer}
          >
            CLOSE
          </button>
        </div>
      </div>
    </div>
  );
};

export default QAInput;

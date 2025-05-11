import React, { useRef, useEffect, useState } from "react";
import "./AdjacentFrame.scss";
import get_adjacent_frame from "../../services/get_adjacent_frame";
import getVideoName from "../../services/get_video_name";
import { NotificationManager } from "react-notifications";

const AdjacentFrame = ({
  page = "pickedFrames",
  listAdjacentFrame,
  middleFrame,
  setIsOpenAdjacentFrame,
  pickedFrames,
  setPickedFrames,
  uploadToTeamPickedFrames,
  setIsUploadConfirming,
}) => {
  const displayRowRef = useRef(null);
  const displayGridRef = useRef(null);
  const middleFrameRef = useRef(null);
  const chooseDurationRef = useRef(null);
  const [duration, setDuration] = useState(10);
  const [loading, setLoading] = useState(false);
  const [adjacentFrames, setAdjacentFrames] = useState(listAdjacentFrame);
  const [pickingFrames, setPickingFrames] = useState([]);
  const [startFrameIndex, setStartFrameIndex] = useState(null); // Vị trí bắt đầu
  const [endFrameIndex, setEndFrameIndex] = useState(null);
  const displayModeRef = useRef(null);
  const [displayMode, setDisplayMode] = useState("LIST"); // Trạng thái checkbox
  const checkDisplayMode = () => {
    if (displayMode === "LIST") {
      setDisplayMode("GRID");
    } else {
      setDisplayMode("LIST");
    }
  };
  const handleDurationChange = (e) => {
    setDuration(e.target.value);
  };

  const scrollToMiddle = (frames) => {
    const adjacentFramesLength = frames.length;
    if (displayRowRef.current) {
      const frameWidth = displayRowRef.current.querySelector(
        ".adjacent-frame-item"
      ).offsetWidth;

      // Calculate the starting position of the 6 frames in the middle
      const startFrameIndex = Math.max(
        0,
        Math.floor(adjacentFramesLength / 2) - 3
      );
      const scrollToPosition =
        frameWidth * startFrameIndex + (startFrameIndex - 1) * 10;

      // Scroll to the calculated position
      displayRowRef.current.scrollLeft = scrollToPosition;
    }
    if (displayGridRef.current) {
      const frameHeight = displayGridRef.current.querySelector(
        ".adjacent-frame-item"
      ).offsetHeight;
      const numberOfLines =
        adjacentFramesLength !== 0 ? Math.ceil(adjacentFramesLength / 6) : 0;
      if (numberOfLines > 4) {
        const startPosition = (numberOfLines - 4) / 2;
        let padding = Math.floor(startPosition);
        padding = Math.max((padding - 2) * 8, 0);
        const scrollToPosition = frameHeight * startPosition + padding;
        displayGridRef.current.scrollTop = scrollToPosition;
      }
      // Scroll to the calculated position
    }
  };

  const fetchAdjacentFrames = async () => {
    setLoading(true);
    try {
      const response = await get_adjacent_frame(
        middleFrame.video_name,
        middleFrame.frame_number,
        duration
      );
      setAdjacentFrames(response.data.frames);
      console.log("adjacent: ", response.data.frames);
      scrollToMiddle(response.data.frames); // Scroll to middle after setting the frames
    } catch (error) {
      console.error("Failed to fetch adjacent frames:", error);
    } finally {
      setLoading(false);
    }
  };

  // const handleCheckboxChange = (event, index, frame) => {
  //   event.stopPropagation();

  //   if (event.target.checked) {
  //     setPickingFrames((prev) => [...prev, frame]); // Thêm frame vào danh sách tạm thời
  //     if (startFrameIndex && index === startFrameIndex - 1) {
  //       setStartFrameIndex(index);
  //     } else if (endFrameIndex && index === endFrameIndex + 1) {
  //       setEndFrameIndex(index);
  //     }
  //   } else {
  //     setPickingFrames(
  //       (prev) => prev.filter((pickingFrame) => pickingFrame.id !== frame.id) // Lọc theo id
  //     ); // Bỏ frame ra khỏi danh sách tạm thời
  //     if (startFrameIndex && index === startFrameIndex + 1) {
  //       setStartFrameIndex(index);
  //     } else if (endFrameIndex && index === endFrameIndex - 1) {
  //       setEndFrameIndex(index);
  //     }
  //   }
  // };

  // const handleMultiSelect = (event, index, frame) => {
  //   event.stopPropagation();
  //   if (startFrameIndex === null) {
  //     // Nếu chưa có start và end, thiết lập vị trí start
  //     setStartFrameIndex(index);

  //     // Mặc định thêm các frame từ start tới cuối mảng
  //     setPickingFrames((prev) => [...prev, ...adjacentFrames.slice(index)]);
  //   } else if (endFrameIndex === null) {
  //     // Nếu đã có start nhưng chưa có end, thiết lập end
  //     setEndFrameIndex(index);

  //     // Lọc các frame từ end tới cuối mảng ra khỏi pickingFrames
  //     setPickingFrames((prev) =>
  //       prev.filter((pickingFrame) => {
  //         const frameIndex = adjacentFrames.findIndex(
  //           (f) => f.id === pickingFrame.id
  //         );
  //         return frameIndex <= index; // Giữ lại các frame trước end
  //       })
  //     );
  //   } else {
  //     setPickingFrames((prev) => {
  //       // Lọc các frame không nằm trong khoảng start tới end
  //       return prev.filter((pickingFrame) => {
  //         const frameIndex = adjacentFrames.findIndex(
  //           (f) => f.id === pickingFrame.id
  //         );
  //         return frameIndex < startFrameIndex || frameIndex > index;
  //       });
  //     });

  //     // Reset start và end để bắt đầu chọn khối mới
  //     setStartFrameIndex(null);
  //     setEndFrameIndex(null);
  //     // handleMultiSelect(event, index, frame); // Gọi lại để thiết lập start mới
  //   }
  // };

  // const uploadToPickedFrames = () => {
  //   // Kiểm tra nếu trong pickedFrames đã có phần tử nào có trường answer
  //   const existingAnswer = pickedFrames.find((frame) => frame.answer)?.answer;

  //   // Lọc pickingFrames để chỉ lấy những frame chưa có trong pickedFrames
  //   const newFrames = pickingFrames.filter(
  //     (pickingFrame) =>
  //       !pickedFrames.some((pickedFrame) => pickedFrame.id === pickingFrame.id)
  //   );

  //   // Nếu đã có answer trong pickedFrames, thêm answer vào những frame mới
  //   const updatedNewFrames = existingAnswer
  //     ? newFrames.map((frame) => ({
  //         ...frame,
  //         answer: existingAnswer,
  //       }))
  //     : newFrames;

  //   // Cập nhật pickedFrames với các frame mới
  //   setPickedFrames((prevPickedFrames) => [
  //     ...prevPickedFrames,
  //     ...updatedNewFrames,
  //   ]);

  //   const updatedNewFramesLength = updatedNewFrames.length;
  //   NotificationManager.success(
  //     `added ${updatedNewFramesLength} frames to picked frames`,
  //     "ADD SUCCESS"
  //   );

  //   // Sau khi upload xong, bạn có thể reset pickingFrames nếu cần
  //   setPickingFrames([]);
  // };

  useEffect(() => {
    scrollToMiddle(listAdjacentFrame); // Initial scroll to middle
  }, [listAdjacentFrame, displayMode]);

  // useEffect(() => {
  //   scrollToMiddle(listAdjacentFrame);
  // })
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        middleFrameRef.current &&
        displayRowRef.current &&
        chooseDurationRef.current &&
        displayModeRef.current &&
        !middleFrameRef.current.contains(event.target) &&
        !displayRowRef.current.contains(event.target) &&
        !chooseDurationRef.current.contains(event.target) &&
        !displayModeRef.current.contains(event.target)
      ) {
        setIsOpenAdjacentFrame(false); // Đóng khi bấm ngoài các vùng xác định
      }
    };

    document.addEventListener("click", handleClickOutside);

    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, [setIsOpenAdjacentFrame]);

  useEffect(() => {
    console.log("picked frames: ", pickedFrames);
  }, [pickedFrames]);

  const setSinglePickedFrame = (event, frame) => {
    event.stopPropagation();
    if (
      pickedFrames.length !== 0 &&
      pickedFrames[0].frame_number === frame.frame_number &&
      pickedFrames[0].video_name === frame.video_name
    ) {
      setPickedFrames([]);
    } else {
      setPickedFrames([frame]);
    }
  };
  return (
    <>
      <div className="overlay"></div>
      <button
        className="button-close"
        onClick={() => {
          setIsOpenAdjacentFrame(false);
        }}
      >
        CLOSE
      </button>
      <div className="display-mode" ref={displayModeRef}>
        <div class="switch">
          <input
            type="checkbox"
            name="input-mode"
            id="input-mode"
            className="input-mode"
            checked={displayMode === "GRID"}
            onChange={checkDisplayMode}
          />
          <span class="slider"></span>
          <p className="list-mode">LIST</p>
          <p className="grid-mode">GRID</p>
        </div>
      </div>
      <button
        className="button-upload"
        onClick={(event) => {
          if (page === "pickedFrames") {
            setIsUploadConfirming(true);
          } else if (page === "teamPickedFrames") {
            uploadToTeamPickedFrames(event, pickedFrames);
          }
        }}
      >
        UPLOAD TO TEAM PICKED
      </button>
      <div className="adjacent-frame">
        <div
          className={`middle-frame ${
            displayMode === "GRID" ? "middle-frame--grid" : null
          } ${
            pickedFrames.some(
              (pickedFrame) =>
                pickedFrame.frame_number === middleFrame.frame_number &&
                pickedFrame.video_name === middleFrame.video_name
            )
              ? "frame-item-group"
              : ""
          }`}
          ref={middleFrameRef}
        >
          <img
            src={`${process.env.REACT_APP_LOCAL_ENDPOINT_FRAMES}/${middleFrame.video_name}/${middleFrame.frame_number}.jpg`}
            alt="adjacent-frame"
            onError={(e) => {
              e.target.onerror = null; // Ngăn sự kiện lặp lại để tránh vòng lặp
              e.target.src = `${process.env.REACT_APP_DEFAULT_ENDPOINT_FRAMES}/${middleFrame.video_name}/${middleFrame.frame_number}.jpg`; // Thay thế bằng ảnh mặc định
            }}
          />
          <div className="metadata">
            <span className="metadata_video-name">
              {middleFrame.video_name}
            </span>
            <span className="metadata_frame-number">
              {middleFrame.frame_number}
            </span>
          </div>
        </div>
        {displayMode === "GRID" && (
          <div className={`display-grid-frame`} ref={displayGridRef}>
            {adjacentFrames.map((adjacentFrame, index) => (
              <div
                className={`adjacent-frame-item  ${
                  pickedFrames.length !== 0 &&
                  pickedFrames[0].frame_number === adjacentFrame.frame_number &&
                  pickedFrames[0].video_name === adjacentFrame.video_name
                    ? "selected-adjacent-frame"
                    : null
                }`}
                onClick={(event) => {
                  setSinglePickedFrame(event, adjacentFrame);
                }}
                // className={`adjacent-frame-item ${
                //   pickedFrames.some(
                //     (pickedFrame) =>
                //       pickedFrame.frame_number === adjacentFrame.frame_number &&
                //       pickedFrame.video_name === adjacentFrame.video_name
                //   )
                //     ? "frame-item-group"
                //     : ""
                // } ${
                //   pickingFrames.some(
                //     (pickingFrame) =>
                //       pickingFrame.frame_number ===
                //         adjacentFrame.frame_number &&
                //       pickingFrame.video_name === adjacentFrame.video_name
                //   )
                //     ? "picking-frame-item-group"
                //     : ""
                // }`}
                key={`${adjacentFrame.video_name}/${adjacentFrame.frame_number}`}
              >
                <img
                  src={`${process.env.REACT_APP_LOCAL_ENDPOINT_FRAMES}/${adjacentFrame.video_name}/${adjacentFrame.frame_number}.jpg`}
                  alt="adjacent-frame"
                  onError={(e) => {
                    e.target.onerror = null; // Ngăn sự kiện lặp lại để tránh vòng lặp
                    e.target.src = `${process.env.REACT_APP_DEFAULT_ENDPOINT_FRAMES}/${adjacentFrame.video_name}/${adjacentFrame.frame_number}.jpg`; // Thay thế bằng ảnh mặc định
                  }}
                />
                <div className="metadata">
                  <span className="metadata_video-name">
                    {adjacentFrame.video_name}
                  </span>
                  <span className="metadata_frame-number">
                    {adjacentFrame.frame_number}
                  </span>
                </div>
                {/* <input
                  type="checkbox"
                  name={`frame-item-check-${index}`}
                  className="frame-item-checkbox"
                  // checked={pickingFrames.some(
                  //   (pickingFrame) =>
                  //     pickingFrame.frame_number ===
                  //       adjacentFrame.frame_number &&
                  //     pickingFrame.video_name === adjacentFrame.video_name
                  // )}
                  // // onChange={(event) => handlePickFrameItem(event, adjacentFrame)}
                  // onChange={(event) =>
                  //   handleCheckboxChange(event, index, adjacentFrame)
                  // }
                  checked={
                    pickedFrames && pickedFrames[0].id === adjacentFrame.id
                  }
                  onChange={(event) => {
                    event.stopPropagation();
                    setPickedFrames([adjacentFrame]);
                  }}
                />
                <div
                  className="cus-checkbox"
                  name={`frame-item-cus-check-${index}`}
                ></div> */}
                <input
                  type="checkbox"
                  name={`select-multi-frame-${index}`}
                  className="select-multi-frame"
                  // checked={pickingFrames.some(
                  //   (pickingFrame) =>
                  //     pickingFrame.frame_number ===
                  //       adjacentFrame.frame_number &&
                  //     pickingFrame.video_name === adjacentFrame.video_name
                  // )}
                  // onChange={(event) =>
                  //   handleMultiSelect(event, index, adjacentFrame)
                  // }
                  checked={
                    pickedFrames.length !== 0 &&
                    pickedFrames[0].frame_number ===
                      adjacentFrame.frame_number &&
                    pickedFrames[0].video_name === adjacentFrame.video_name
                  }
                  onChange={(event) => {
                    setSinglePickedFrame(event, adjacentFrame);
                  }}
                />
                <div
                  className="cus-multi-select"
                  // name={`frame-item-cus-check-${index}`}
                ></div>
              </div>
            ))}
          </div>
        )}
        {displayMode === "LIST" && (
          <div
            className={`display-row-frame custom-scroll `}
            ref={displayRowRef}
          >
            {adjacentFrames.map((adjacentFrame, index) => (
              <div
                className={`adjacent-frame-item  ${
                  pickedFrames.length !== 0 &&
                  pickedFrames[0].frame_number === adjacentFrame.frame_number &&
                  pickedFrames[0].video_name === adjacentFrame.video_name
                    ? "selected-adjacent-frame"
                    : null
                }`}
                onClick={(event) => {
                  setSinglePickedFrame(event, adjacentFrame);
                }}
                // className={`adjacent-frame-item
                //   ${
                //   pickedFrames.some(
                //     (pickedFrame) =>
                //       pickedFrame.frame_number === adjacentFrame.frame_number &&
                //       pickedFrame.video_name === adjacentFrame.video_name
                //   )
                //     ? "frame-item-group"
                //     : ""
                // } ${
                //   pickingFrames.some(
                //     (pickingFrame) =>
                //       pickingFrame.frame_number ===
                //         adjacentFrame.frame_number &&
                //       pickingFrame.video_name === adjacentFrame.video_name
                //   )
                //     ? "picking-frame-item-group"
                //     : ""
                //   }
                //     `}
                key={`${adjacentFrame.video_name}/${adjacentFrame.frame_number}`}
                // onClick={(event) => {
                //   event.stopPropagation();
                //   if (pickedFrames && pickedFrames[0].id === adjacentFrame.id) {
                //     setPickedFrames([]);
                //   } else {
                //     setPickedFrames([adjacentFrame]);
                //   }
                // }}
              >
                <img
                  src={`${process.env.REACT_APP_LOCAL_ENDPOINT_FRAMES}/${adjacentFrame.video_name}/${adjacentFrame.frame_number}.jpg`}
                  alt="adjacent-frame"
                  onError={(e) => {
                    // console.log(
                    //   "end point: ",
                    //   process.env.REACT_APP_DEFAULT_ENDPOINT_FRAMES
                    // );
                    e.target.onerror = null; // Ngăn sự kiện lặp lại để tránh vòng lặp
                    e.target.src = `${process.env.REACT_APP_DEFAULT_ENDPOINT_FRAMES}/${adjacentFrame.video_name}/${adjacentFrame.frame_number}.jpg`; // Thay thế bằng ảnh mặc định
                  }}
                />
                <div className="metadata">
                  <span className="metadata_video-name">
                    {adjacentFrame.video_name}
                  </span>
                  <span className="metadata_frame-number">
                    {adjacentFrame.frame_number}
                  </span>
                </div>
                {/* <input
                  type="checkbox"
                  name={`frame-item-check-${index}`}
                  className="frame-item-checkbox"
                  checked={pickingFrames.some(
                    (pickingFrame) =>
                      pickingFrame.frame_number ===
                        adjacentFrame.frame_number &&
                      pickingFrame.video_name === adjacentFrame.video_name
                  )}
                  // onChange={(event) => handlePickFrameItem(event, adjacentFrame)}
                  onChange={(event) =>
                    handleCheckboxChange(event, index, adjacentFrame)
                  }
                />
                <div
                  className="cus-checkbox"
                  name={`frame-item-cus-check-${index}`}
                ></div> */}
                <input
                  type="checkbox"
                  name={`select-multi-frame-${index}`}
                  className="select-multi-frame"
                  // checked={pickingFrames.some(
                  //   (pickingFrame) =>
                  //     pickingFrame.frame_number ===
                  //       adjacentFrame.frame_number &&
                  //     pickingFrame.video_name === adjacentFrame.video_name
                  // )}
                  // onChange={(event) =>
                  //   handleMultiSelect(event, index, adjacentFrame)
                  // }
                  checked={
                    pickedFrames.length !== 0 &&
                    pickedFrames[0].frame_number ===
                      adjacentFrame.frame_number &&
                    pickedFrames[0].video_name === adjacentFrame.video_name
                  }
                  onChange={(event) => {
                    setSinglePickedFrame(event, adjacentFrame);
                  }}
                />
                <div
                  className="cus-multi-select"
                  // name={`frame-item-cus-check-${index}`}
                ></div>
              </div>
            ))}
          </div>
        )}

        <div
          className={`choose-duration ${
            displayMode === "GRID" ? "choose-duration--grid" : null
          }`}
          ref={chooseDurationRef}
        >
          <label htmlFor="duration">Enter Duration (seconds):</label>
          <div className="wrap-button">
            <input
              type="number"
              id="duration"
              name="duration"
              min="1"
              value={duration}
              onChange={handleDurationChange}
              required
            />
            <button
              type="submit"
              onClick={fetchAdjacentFrames}
              disabled={loading}
            >
              {loading ? "Loading..." : "Get"}
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default AdjacentFrame;

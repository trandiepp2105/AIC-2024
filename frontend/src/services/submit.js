import axios from "axios";
const submitEndpoint = `https://eventretrieval.one/api/v2/submit`;

// Hàm tính thời gian từ frame number và fps
const calculateTimeFromFrame = (frameNumber, fps) => {
  return Math.round((frameNumber / fps) * 1000); // Tính thời gian từ frame số ra mili giây
};

const submit = async (queryMode, video_name, frame_number, fps, answer) => {
  // Lấy evaluationID và sessionID từ localStorage
  const evaluationID = localStorage.getItem("evaluationID");
  const sessionID = localStorage.getItem("sessionID");

  // Kiểm tra nếu evaluationID hoặc sessionID không tồn tại
  if (!evaluationID || !sessionID) {
    console.error(
      "Evaluation ID hoặc Session ID không tồn tại trong localStorage."
    );
    return null;
  }

  // Tính thời gian từ frame number và fps
  const time = calculateTimeFromFrame(frame_number, fps);

  // Xác định body dựa trên queryMode
  let body = {};
  if (queryMode === "QA") {
    body = {
      answerSets: [
        {
          answers: [
            {
              text: `${answer}-${video_name}-${time}`,
            },
          ],
        },
      ],
    };
  } else if (queryMode === "TEXT") {
    body = {
      answerSets: [
        {
          answers: [
            {
              mediaItemName: video_name,
              start: time,
              end: time,
            },
          ],
        },
      ],
    };
  } else {
    console.error("Invalid queryMode provided. Expected 'QA' or 'TEXT'.");
    return null;
  }

  try {
    const response = await axios.post(
      `${submitEndpoint}/${evaluationID}`,
      body,
      {
        params: {
          session: sessionID,
        },
      }
    );
    const { data } = response;
    if (data) {
      return data; // Trả về dữ liệu nếu tồn tại
    } else {
      console.error("Không có dữ liệu trả về từ API.");
      return null;
    }
  } catch (error) {
    console.error("Error occurred while getting evaluation ID:", error);
    throw error;
  }
};

export default submit;

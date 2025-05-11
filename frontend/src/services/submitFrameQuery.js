import axios from "axios";

const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/submit/`;

const submitFrameQuery = async (
  queryMode,
  video_name,
  frame_number,
  answer
) => {
  const submitQuery = {
    query_mode: queryMode,
    video_name: video_name,
    frame_number: frame_number,
    answer: answer,
  };
  try {
    const response = await axios.post(endpoint, submitQuery);
    const { data } = response;
    if (data) {
      return data; // Trả về dữ liệu nếu tồn tại
    } else {
      console.error("SUBMIT KHÔNG THÀNH CÔNG.");
      return null;
    }
  } catch (error) {
    console.error("Error occurred while submit:", error);
    throw error;
  }
};

export default submitFrameQuery;

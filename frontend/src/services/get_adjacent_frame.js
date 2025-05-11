import axios from "axios";
const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/frames/adjacent/`;
const get_adjacent_frame = async (video_name, frame_number, duration = 10) => {
  try {
    const response = await axios.get(endpoint, {
      headers: {
        "Content-Type": "application/json",
      },
      params: {
        video_name,
        frame_number,
        duration,
      },
    });
    console.log("Get get adjacent frames successfully");
    return response;
  } catch (error) {
    console.error("Error occurred while get adjacent frames:", error);
    throw error;
  }
};

export default get_adjacent_frame;

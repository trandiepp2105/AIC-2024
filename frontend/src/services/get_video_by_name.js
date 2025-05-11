import axios from "axios";
const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/videos/`;
const get_video_by_name = async (video_name) => {
  try {
    const response = await axios.get(endpoint, {
      params: { video_name: video_name },
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("Get video successfully");
    return response;
  } catch (error) {
    console.error("Error occurred while Get video:", error);
    throw error;
  }
};

export default get_video_by_name;

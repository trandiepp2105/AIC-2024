import axios from "axios";
const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/videos/`;
const get_video = async (video_id) => {
  try {
    const response = await axios.get(endpoint + video_id, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("Get video successfully");
    return response;
  } catch (error) {
    console.error("Error occurred while Get classes:", error);
    throw error;
  }
};

export default get_video;

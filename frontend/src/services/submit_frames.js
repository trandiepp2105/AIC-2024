import axios from "axios";
const ENDPOINT = "http://endpoint";

const submit_frames = async (frames) => {
  try {
    const response = await axios.post(ENDPOINT, frames, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    return response;
  } catch (error) {}
};

export default submit_frames;

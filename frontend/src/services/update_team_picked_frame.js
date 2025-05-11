import axios from "axios";
const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/team-picked-frame/`;

async function updateTeamPickedFrame(data) {
  try {
    const response = await axios.put(endpoint, data);
    return response;
  } catch (error) {
    console.error("Error updating frame data:", error);
    throw error;
  }
}

export default updateTeamPickedFrame;

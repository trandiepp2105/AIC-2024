import axios from "axios";
const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/team-picked-frame/delete-by-query-index/`;

async function deleteTeamPickedFrameByIndex(queryIndex) {
  try {
    const response = await axios.delete(`${endpoint}${queryIndex}`);
    return response;
  } catch (error) {
    console.error(
      "Error:",
      error.response ? error.response.data : error.message
    );
    throw error;
  }
}

export default deleteTeamPickedFrameByIndex;

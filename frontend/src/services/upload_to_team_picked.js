import axios from "axios";
const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/team-picked-frame/`;

// Định nghĩa hàm để post danh sách TeamPickedFrameBase lên endpoint
async function postTeamPickedFrames(teamPickedFrames) {
  try {
    // Thực hiện POST request đến endpoint của FastAPI
    const response = await axios.post(endpoint, teamPickedFrames, {
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Xử lý phản hồi từ server
    console.log("UPLOAD SUCCESS!");
    return response;
  } catch (error) {
    // Xử lý lỗi nếu request thất bại
    console.error(
      "Error:",
      error.response ? error.response.data : error.message
    );
    throw error;
  }
}

export default postTeamPickedFrames;

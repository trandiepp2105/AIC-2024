import axios from "axios";
const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/team-picked-frame/`;

// Định nghĩa hàm để post danh sách TeamPickedFrameBase lên endpoint
async function getTeamPickedFrames(query_index = null, mode = null) {
  try {
    // Thực hiện POST request đến endpoint của FastAPI
    const response = await axios.get(endpoint, {
      headers: {
        "Content-Type": "application/json",
      },
      params: {
        query_index: query_index,
        mode: mode,
      },
    });

    // Xử lý phản hồi từ server
    // console.log("GET TEAM PICKED SUCCESS!");
    return response;
  } catch (error) {
    // Xử lý lỗi nếu request thất bại
    console.error(
      "Error:",
      error.response ? error.response.data : error.message
    );
    // throw error;
  }
}

export default getTeamPickedFrames;

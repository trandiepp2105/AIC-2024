import axios from "axios";

// Đảm bảo endpoint được cấu hình đúng
const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/team-picked-frame/update-answer`;

async function updateQAAnswer(frameId, newAnswer) {
  console.log("new answer: ", newAnswer);
  console.log("id: ", frameId);
  try {
    // Gửi yêu cầu PUT với dữ liệu cập nhật (frameId và newAnswer)
    const response = await axios.put(`${endpoint}/${frameId}`, null, {
      params: { new_answer: newAnswer }, // Gửi new_answer dưới dạng query parameter
    });

    // Kiểm tra phản hồi từ API và trả về dữ liệu nếu thành công
    if (response.status === 200) {
      console.log("Answer updated successfully");
      return response; // Trả về dữ liệu phản hồi nếu cần sử dụng
    } else {
      console.error("Failed to update answer. Status:", response.status);
      throw new Error("Failed to update answer");
    }
  } catch (error) {
    // Xử lý lỗi trong quá trình gửi yêu cầu
    if (error.response) {
      console.error("Error from API:", error.response.data);
      throw new Error(error.response.data.detail || "Error updating answer");
    } else if (error.request) {
      console.error("No response from API:", error.request);
      throw new Error("No response from server");
    } else {
      console.error("Request error:", error.message);
      throw new Error("Error updating frame data");
    }
  }
}

export default updateQAAnswer;

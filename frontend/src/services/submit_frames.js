import axios from "axios";
import submit from "./submit";

const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/submit/`;

function createCSV(frames, mode) {
  const rows = [];
  // Thêm tiêu đề cho các cột, bao gồm cột số thứ tự
  // rows.push(["video_name", "frame_number", "answer"]);

  frames.forEach((frame, idx) => {
    if (mode === "QA") {
      rows.push([frame.video_name, frame.frame_number, frame.answer]);
    } else {
      rows.push([frame.video_name, frame.frame_number]);
    }
  });

  const csvContent = rows.map((e) => e.join(",")).join("\n");
  return new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
}

const submitFrames = async (frames, mode, queryIndex) => {
  const blob = createCSV(frames, mode);
  const type = mode === "TEXT" ? "kis" : "qa";
  // Tạo một liên kết để tải tệp CSV về máy tính
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `query-p3-${queryIndex}-${type}.csv`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);

  // Gửi file lên server
  const formData = new FormData();
  formData.append("file", blob, `query-${queryIndex}-${type}.csv`);

  try {
    const response = await axios.post(endpoint, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response;
  } catch (error) {
    console.error("error: ", error);
    throw error;
  }
};

export default submitFrames;

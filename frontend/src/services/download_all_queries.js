import JSZip from "jszip";
import getTeamPickedFrames from "./get_team_picked";

function createCSV(frames, mode) {
  const rows = [];
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

const download_all_query = async (start = 1, end) => {
  const zip = new JSZip();
  const promises = [];

  if (!end) {
    // Nếu chỉ có start mà không có end, xử lý trường hợp này
    const res = await getTeamPickedFrames(start);
    if (res && res.status >= 200 && res.status < 300) {
      const blob = createCSV(res.data, res.data[0].mode);
      const type = res.data[0].mode === "TEXT" ? "kis" : "qa";
      zip.file(`query-p3-${start}-${type}.csv`, blob);
    }
  } else {
    for (let i = start; i <= end; i++) {
      console.log("download query: ", i);
      promises.push(
        (async (index) => {
          const res = await getTeamPickedFrames(index);
          if (res && res.status >= 200 && res.status < 300) {
            const blob = createCSV(res.data, res.data[0].mode);
            const type = res.data[0].mode === "TEXT" ? "kis" : "qa";
            zip.file(`query-p3-${index}-${type}.csv`, blob);
          }
        })(i)
      );
    }
    await Promise.all(promises); // Đợi tất cả các yêu cầu hoàn thành
  }

  // Tạo tệp ZIP và tải về
  zip.generateAsync({ type: "blob" }).then((content) => {
    const url = URL.createObjectURL(content);
    const link = document.createElement("a");
    link.href = url;
    link.download = "queries.zip";
    link.click();
    URL.revokeObjectURL(url); // Giải phóng URL sau khi tải xong
  });
};

export default download_all_query;

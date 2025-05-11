function extractVideoName(url) {
  // Sử dụng regex để tìm phần tên video trong URL
  const regex = /\/frames\/([^/]+)\//;

  const match = url.match(regex);

  if (match && match[1]) {
    return match[1];
  } else {
    return null; // Trường hợp không tìm thấy tên video
  }
}

export default extractVideoName;

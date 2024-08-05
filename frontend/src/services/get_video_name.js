const getVideoName = (url) => {
  const videoNameWithExtension = url.substring(url.lastIndexOf("/") + 1);
  const videoName = videoNameWithExtension.replace(".mp4", "");
  return videoName;
};

export default getVideoName;

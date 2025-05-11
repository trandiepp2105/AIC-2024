function calculateFrameTime(frameNumber, fps) {
  if (fps <= 0) {
    throw new Error("FPS phải lớn hơn 0");
  }
  const timeInSeconds = frameNumber / fps;
  return timeInSeconds;
}

export default calculateFrameTime;

import React, { useState, useRef, useEffect } from "react";
import ReactPlayer from "react-player";
import "./VideoPlayer.scss";

const VideoPlayer = ({ startTime = 0, videoPath, handleClosePlayerVideo }) => {
  const [playing, setPlaying] = useState(true);
  const [played, setPlayed] = useState(0);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [timeToSkip, setTimeToSkip] = useState(2);
  const playerRef = useRef(null);
  const playerVideoContainer = useRef(null);
  const videoTimeRef = useRef(null);

  const handlePlayPause = (e) => {
    e.stopPropagation(); // Ngăn chặn sự kiện click lan ra ngoài
    setPlaying(!playing);
  };

  const handleProgress = (state) => {
    setPlayed(state.played);
    setCurrentTime(playerRef.current.getCurrentTime());
  };

  const handleDuration = (duration) => {
    setDuration(duration);
  };

  const handleSeekChange = (e) => {
    const value = parseFloat(e.target.value);
    setPlayed(value);
    playerRef.current.seekTo(value);
    updateSliderBackground(value);
  };

  const updateSliderBackground = (value) => {
    const videoTimeElement = videoTimeRef.current;
    if (videoTimeElement) {
      const progress = (value / videoTimeElement.max) * 100;
      videoTimeElement.style.background = `linear-gradient(to right, #f50 ${progress}%, #ccc ${progress}%)`;
    }
  };

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs < 10 ? "0" : ""}${secs}`;
  };

  const handleKeyDown = (event) => {
    const currentTimeVid = playerRef.current?.getCurrentTime();

    // Kiểm tra nếu currentTimeVid, timeToSkip, và duration đều là số hợp lệ
    if (
      !Number.isFinite(currentTimeVid) ||
      !Number.isFinite(timeToSkip) ||
      !Number.isFinite(duration)
    ) {
      console.error("Invalid currentTimeVid, timeToSkip, or duration");
      return;
    }

    let newTime = currentTimeVid;

    if (event.key === "ArrowRight") {
      event.preventDefault();
      newTime = Math.min(currentTimeVid + timeToSkip, duration);
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      newTime = Math.max(currentTimeVid - timeToSkip, 0);
    }

    // Kiểm tra xem newTime có phải là số hợp lệ
    if (Number.isFinite(newTime) && newTime >= 0) {
      setCurrentTime(newTime);
      // Chuyển thành seekTo newTime trực tiếp
      playerRef.current.seekTo(newTime);
    } else {
      console.error("Invalid newTime after calculation:", newTime);
    }
  };

  useEffect(() => {
    if (startTime > 0 && playerRef.current) {
      playerRef.current.seekTo(startTime);
      setPlayed(startTime / duration); // Update the played state based on the startTime
      setPlaying(true); // Start playing the video
    }
  }, [startTime, duration]); // Run this effect when startTime or duration changes

  // Update the slider background when the `played` value changes
  useEffect(() => {
    updateSliderBackground(played);
  }, [played]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        playerVideoContainer.current &&
        !playerVideoContainer.current.contains(event.target)
      ) {
        handleClosePlayerVideo();
      }
    };

    document.addEventListener("click", handleClickOutside);
    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("click", handleClickOutside);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [handleClosePlayerVideo, handleKeyDown]);

  // useEffect(() => {
  //   console.log("duration: ", duration);
  //   console.log(playerRef.current.getCurrentTime());
  // }, [currentTime]);
  return (
    <div
      className="video-player"
      ref={playerVideoContainer}
      onClick={handlePlayPause}
    >
      <div className="wrap-time-to-skip">
        Time to skip:{" "}
        <input
          type="number"
          onChange={(event) => {
            const time = event.target.value;
            setTimeToSkip(time);
          }}
          value={timeToSkip}
        />
      </div>
      <ReactPlayer
        className="video-area"
        ref={playerRef}
        url={videoPath}
        // url="https://www.youtube.com/watch?v=LXb3EKWsInQ"
        playing={playing}
        onProgress={handleProgress}
        onDuration={handleDuration}
        controls={false} // Disable default controls
        onPlay={() => setPlaying(true)}
        onPause={() => setPlaying(false)}
      />
      <div className="controls">
        <button onClick={handlePlayPause} className="pause-button">
          {playing ? (
            <svg
              width="800px"
              height="800px"
              viewBox="0 0 24 24"
              fill="#f50"
              xmlns="http://www.w3.org/2000/svg"
              className="icon"
            >
              <path d="M9 6a1 1 0 0 1 1 1v10a1 1 0 1 1-2 0V7a1 1 0 0 1 1-1zm6 0a1 1 0 0 1 1 1v10a1 1 0 1 1-2 0V7a1 1 0 0 1 1-1z" />
            </svg>
          ) : (
            <svg
              fill="#f50"
              width="800px"
              height="800px"
              viewBox="-60 0 512 512"
              xmlns="http://www.w3.org/2000/svg"
              className="icon"
            >
              <title>{"play"}</title>
              <path d="M64 96L328 256 64 416 64 96Z" />
            </svg>
          )}
        </button>
        <input
          type="range"
          min={0}
          max={1}
          step="any"
          value={played}
          onChange={handleSeekChange}
          ref={videoTimeRef}
          onClick={(e) => e.stopPropagation()} // Ngăn chặn sự kiện click lan ra ngoài
        />
        <div className="video-time">
          {formatTime(currentTime)} / {formatTime(duration)}
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;

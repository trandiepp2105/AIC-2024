import React, { useState, useRef, useEffect } from "react";
import "./ResultInterface.scss";
import download_all_query from "../../services/download_all_queries";
import getTeamPickedFrames from "../../services/get_team_picked";
import { useHomeContext } from "../../pages/home-page/HomePage";
import submitFrames from "../../services/submit_frames";
import { NotificationManager } from "react-notifications";
const ResultInterface = ({
  getAllQueryResults,
  queryResults,
  setQueryResults,
}) => {
  const {
    queryIndex,
    queryMode,
    setQueryIndex,
    setQueryMode,
    setBrowsingOption,
    handleDeleteTeamPickedFrameByIndex,
  } = useHomeContext();
  const listBrowsingOption = {
    browsing: "browsing",
    picked: "picked",
    teamPicked: "team-picked",
  };

  const [isDeleteConfirming, setIsDeleteComfirming] = useState(false);
  const [startDownloadIndex, setStartDownloadIndex] = useState(1);
  const [endDownloadIndex, setEndDownloadIndex] = useState(1);
  const [isDownloadConfirming, setIsDownloadConfirming] = useState(false);
  const [activeResultQueryIndex, setActiveResultQueryIndex] = useState(null);
  const downloadConfirmRef = useRef(null);
  const downloadConfirmInnerRef = useRef(null);

  const handleDownloadAllQueries = () => {
    download_all_query(startDownloadIndex, endDownloadIndex);
  };

  const handleDelete = async (e, currentQueryIndex) => {
    e.stopPropagation(); // Ngăn chặn sự kiện lan truyền
    await handleDeleteTeamPickedFrameByIndex(e, currentQueryIndex);
    getAllQueryResults();
  };

  const handleDownload = async (e, teamPickedFrames) => {
    e.stopPropagation(); // Ngăn chặn sự kiện lan truyền
    if (teamPickedFrames.length > 0) {
      const response = await submitFrames(
        teamPickedFrames,
        queryMode,
        queryIndex
      );
      if (response.status === 200) {
        NotificationManager.success("Submit successfully", "SUBMIT", 3000);
      } else {
        NotificationManager.error("Submit failed", "SUBMIT", 3000);
      }
    }
  };

  useEffect(() => {
    getAllQueryResults();
  }, []);
  useEffect(() => {
    console.log("query results: ", queryResults);
  }, [queryResults]);
  return (
    <div className="result-interface">
      {isDeleteConfirming && (
        <div className="submit-confirm">
          <div className="overlay"></div>
          <div className="confirm-popup">
            <div className="confirm-popup__header">
              <p>Confirm</p>
              <span
                className="close-button"
                onClick={() => {
                  setIsDeleteComfirming(false);
                }}
              >
                &times;
              </span>
            </div>
            <div className="confirm-popup__content">
              Confirm you want to delete query
              <span className="query-index">{queryIndex}</span>?
            </div>
            <div className="confirm-popup__buttons">
              <button
                className="confirm-button confirm-button--no"
                onClick={() => {
                  setIsDeleteComfirming(false);
                }}
              >
                CLOSE
              </button>

              <button
                className="confirm-button confirm-button--yes"
                // onClick={confirmSubmit}
                onClick={async (event) => {
                  // confirmSubmit(teamPickedFrames);
                  await handleDelete(event, queryIndex);
                  setIsDeleteComfirming(false);
                }}
              >
                DELETE
              </button>
            </div>
          </div>
        </div>
      )}
      <div className="container">
        <div className="button-block">
          <button
            className="download-button"
            onClick={() => setIsDownloadConfirming(true)}
          >
            Download
          </button>
          <button className="clear-button">Clear</button>
        </div>
        <div className="wrapper-result">
          {queryResults.map((resultRow, resultRowIndex) => {
            return (
              <div
                className={`result-item ${
                  resultRow[0].query_index === activeResultQueryIndex
                    ? "active-result-item"
                    : null
                }`}
                onClick={(event) => {
                  event.stopPropagation();
                  setBrowsingOption(listBrowsingOption.teamPicked);
                  setQueryIndex(resultRow[0].query_index);
                  setQueryMode(resultRow[0].mode);

                  setActiveResultQueryIndex(resultRow[0].query_index);
                }}
              >
                <div className="result-item__general">
                  <p className="query-index">
                    Index: <span>{resultRow[0].query_index}</span> Mode:{" "}
                    <span>{resultRow[0].mode}</span>
                  </p>
                  <div className="result-btn-block">
                    <button
                      className="result-btn"
                      onClick={(event) => {
                        // handleDelete(event, resultRow[0].query_index);
                        setIsDeleteComfirming(true);
                      }}
                    >
                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        className="delete-svg"
                      >
                        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                        <g
                          id="SVGRepo_tracerCarrier"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        ></g>
                        <g id="SVGRepo_iconCarrier">
                          {" "}
                          <path
                            d="M6 7V18C6 19.1046 6.89543 20 8 20H16C17.1046 20 18 19.1046 18 18V7M6 7H5M6 7H8M18 7H19M18 7H16M10 11V16M14 11V16M8 7V5C8 3.89543 8.89543 3 10 3H14C15.1046 3 16 3.89543 16 5V7M8 7H16"
                            stroke="#000000"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          ></path>{" "}
                        </g>
                      </svg>
                    </button>
                    <button
                      className="result-btn"
                      onClick={(event) => {
                        handleDownload(event, resultRow);
                      }}
                    >
                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        className="download-svg"
                      >
                        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                        <g
                          id="SVGRepo_tracerCarrier"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        ></g>
                        <g id="SVGRepo_iconCarrier">
                          {" "}
                          <g id="Interface / Download">
                            {" "}
                            <path
                              id="Vector"
                              d="M6 21H18M12 3V17M12 17L17 12M12 17L7 12"
                              stroke="#000000"
                              stroke-width="2"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                            ></path>{" "}
                          </g>{" "}
                        </g>
                      </svg>
                    </button>
                  </div>
                </div>
                <div className="result-item__detail">
                  <p className="result-quantity">
                    Quantity: <span>{resultRow.length}</span>
                  </p>
                  {resultRow[0].mode === "QA" && (
                    <p className="first-answer">
                      First Answer: <span>{resultRow[0].answer}</span>
                    </p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
        <span className="padding-box"> </span>
      </div>
      {isDownloadConfirming && (
        <div className="download-confirm" ref={downloadConfirmRef}>
          <div className="inner" ref={downloadConfirmInnerRef}>
            <p className="title">Do you want to download all queries?</p>
            <div className="pick-queries">
              <div className="pick-queries--item">
                <p className="label">START</p>
                <input
                  type="number"
                  onChange={(event) => {
                    const index = event.target.value;
                    setStartDownloadIndex(index);
                  }}
                  value={startDownloadIndex}
                />
              </div>
              <div className="pick-queries--item">
                <p className="label">END</p>
                <input
                  type="number"
                  onChange={(event) => {
                    const index = event.target.value;
                    setEndDownloadIndex(index);
                  }}
                  value={endDownloadIndex}
                />
              </div>
            </div>
            <div className="download-services">
              <button className="download" onClick={handleDownloadAllQueries}>
                Download
              </button>
              <button
                className="close"
                onClick={() => {
                  setIsDownloadConfirming(false);
                }}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultInterface;

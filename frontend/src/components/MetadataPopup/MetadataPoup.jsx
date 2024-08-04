import React from "react";
import "./MetadataPopup.scss";
const MetadataPoup = ({ videoName = "video name", frameNumber = 1024 }) => {
  return (
    <div className="metadata-popup">
      {/* <div className="metadata-popup__header">METADATA</div> */}
      <div className="metadata-popup__content">
        <div className="metadata-popup__item">
          <p className="item__title">Video name:</p>
          <p className="item__value">{videoName}</p>
        </div>
        <div className="metadata-popup__item">
          <p className="item__title">Frame number:</p>
          <p className="item__value">{frameNumber}</p>
        </div>
      </div>
    </div>
  );
};

export default MetadataPoup;

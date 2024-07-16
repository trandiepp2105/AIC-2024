import React from "react";
import axios from "axios";
import "./SearchInterface.scss";
import ColorPicker from "../ColorPicker/ColorPicker";
import { useSearchData } from "../../pages/home-page/HomePage";
const SearchInterface = () => {
  const { searchData, setSearchData, initialSearchData } = useSearchData();
  const handleChangeSearchData = (e) => {
    const { name, value } = e.target;
    setSearchData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const resetSearchData = () => {
    setSearchData(initialSearchData);
  };
  const handleSubmit = async () => {
    console.log("data:", searchData);
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/search/",
        searchData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log("Response:", response.data);
    } catch (error) {
      console.error("Error sending data:", error);
    }
  };
  return (
    <div className="search-interface">
      <div className="container">
        <div className="wrapper-raw-text-area">
          <textarea
            name="rawText"
            id="raw-text"
            className="raw-text-area"
            placeholder="enter key search"
            onChange={handleChangeSearchData}
            value={searchData.rawText}
          />
        </div>
        <div className="wrapper-search-by-task-area">
          <div className="task-item">
            <label htmlFor="object" className="label-task">
              Object
            </label>
            <input
              type="text"
              name="object"
              id="object"
              className="task-content"
              value={searchData.object}
              onChange={handleChangeSearchData}
            />
          </div>
          <div className="task-item">
            <label htmlFor="predicate" className="label-task">
              Predicate
            </label>
            <input
              type="text"
              name="predicate"
              id="predicate"
              className="task-content"
              value={searchData.predicate}
              onChange={handleChangeSearchData}
            />
          </div>
          <div className="task-item">
            <label htmlFor="quantity" className="label-task">
              Quantity
            </label>
            <input
              type="text"
              name="quantity"
              id="quantity"
              className="task-content"
              value={searchData.quantity}
              onChange={handleChangeSearchData}
            />
          </div>
          <div className="task-item">
            <label htmlFor="time" className="label-task">
              Time
            </label>
            <input
              type="text"
              name="time"
              id="time"
              className="task-content"
              value={searchData.time}
              onChange={handleChangeSearchData}
            />
          </div>
          <div className="task-item">
            <label htmlFor="location" className="label-task">
              Location
            </label>
            <input
              type="text"
              name="location"
              id="location"
              className="task-content"
              value={searchData.location}
              onChange={handleChangeSearchData}
            />
          </div>
        </div>

        <div className="button-block">
          <button className="search-button" onClick={handleSubmit}>
            Search
          </button>
          <button className="clear-button" onClick={resetSearchData}>
            Clear
          </button>
        </div>

        <div className="wrapper-frame-selected" id="wrapper-frame-selected">
          <div className="title">Frame select</div>
          <div className="content"></div>
        </div>

        <div className="wrapper-color-picker">
          <ColorPicker />
        </div>
      </div>
    </div>
  );
};

export default SearchInterface;

import React, { useCallback, useEffect } from "react";
import "./SearchInterface.scss";
import ColorPicker from "../ColorPicker/ColorPicker";
import { useHomeContext } from "../../pages/home-page/HomePage";

const SearchInterface = () => {
  const { searchData, setSearchData, initialSearchData, handleSearchText } =
    useHomeContext();

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

  // Memoize handleSubmit to avoid recreation on every render
  const handleSubmit = useCallback(async () => {
    await handleSearchText(searchData);
    // Làm mất focus khỏi tất cả các trường nhập liệu
    const focusedElement = document.activeElement;
    if (focusedElement) {
      focusedElement.blur();
    }
  }, [searchData, handleSearchText]);

  // Memoize handleKeyDown to avoid recreation on every render
  const handleKeyDown = useCallback(
    (e) => {
      // Kiểm tra phần tử hiện tại có focus hay không
      const focusedElement = document.activeElement;
      const isInputOrTextarea =
        focusedElement.tagName === "TEXTAREA" ||
        focusedElement.tagName === "INPUT";

      if (e.key === "Enter") {
        if (e.shiftKey) {
          // Nếu Shift + Enter thì xuống dòng
          e.preventDefault();
          if (focusedElement.tagName === "TEXTAREA") {
            const cursorPosition = focusedElement.selectionStart;
            const value = focusedElement.value;
            focusedElement.value =
              value.substring(0, cursorPosition) +
              "\n" +
              value.substring(cursorPosition);
            focusedElement.selectionStart = cursorPosition + 1;
            focusedElement.selectionEnd = cursorPosition + 1;
            setSearchData((prevData) => ({
              ...prevData,
              rawText: focusedElement.value,
            }));
          }
        } else if (isInputOrTextarea) {
          // Nếu chỉ Enter thì submit
          e.preventDefault();
          handleSubmit();
        }
      }
    },
    [handleSubmit, setSearchData]
  );

  useEffect(() => {
    // Thêm sự kiện keydown vào document khi component mount
    document.addEventListener("keydown", handleKeyDown);

    // Xóa sự kiện khi component unmount
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [handleKeyDown]); // Phụ thuộc vào handleKeyDown để đảm bảo sự kiện được cập nhật

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

import React, { useCallback, useEffect, useState } from "react";
import "./SearchInterface.scss";
import ColorPicker from "../ColorPicker/ColorPicker";
import { useHomeContext } from "../../pages/home-page/HomePage";
import ColorZone from "../ColorZone/ColorZone";
import Slider from "../Slider/Slider";
// import { translate } from "@vitalets/google-translate-api";
// import translate from "google-translate-api-x";
// import translateText from "../../services/translate";
import { translate } from "@vitalets/google-translate-api";
const SearchInterface = () => {
  const [currentColor, setCurrentColor] = useState("#4093e6");
  const [pastedImage, setPastedImage] = useState(null);
  const { searchData, setSearchData, initialSearchData, handleSearchText } =
    useHomeContext();

  const handleChangeSearchData = async (e) => {
    const { name, value } = e.target;

    if (name == "rawText") {
      // try {
      //   const { text } = await translate("Привет, мир! Как дела?", {
      //     to: "en",
      //   });
      //   console.log(text);
      // } catch (err) {
      //   console.error(err);
      // }
    }
    setSearchData((prevData) => ({
      ...prevData,
      [name]: {
        ...prevData[name],
        value: value,
      },
    }));
  };

  const handleChangePriority = (event) => {
    function convertText(text) {
      // ex: text = raw-text-priority
      // Chia chuỗi đầu vào thành mảng các phần tử bằng dấu gạch ngang
      const parts = text.split("-");

      // Lấy phần tử cuối cùng và loại bỏ từ 'priority'
      const lastPart = parts.pop().replace("priority", "");

      // Chuyển đổi các phần tử còn lại thành chữ hoa chữ cái đầu tiên và nối lại
      const capitalizedParts = parts
        .map((part, index) => {
          // Chỉ chuyển đổi các phần tử không phải đầu tiên
          if (index === 0) {
            return part; // Giữ nguyên phần tử đầu tiên
          }
          return part.charAt(0).toUpperCase() + part.slice(1); // Chữ hoa phần tử khác
        })
        .join("");

      // Ghép phần tử đã chuyển đổi với phần tử cuối cùng
      return capitalizedParts + lastPart;
    }

    const { name, value } = event.target;
    const field_name = convertText(name);
    console.log(`Name: ${field_name}, Priority: ${value}`);
    setSearchData((prevData) => {
      const newSearchData = {
        ...prevData,
        [field_name]: {
          ...prevData[field_name],
          priority: parseInt(value),
        },
      };
      return newSearchData;
    });
  };
  const resetSearchData = () => {
    setSearchData(initialSearchData);
    setPastedImage(null);
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

  // Handle paste event to get the image
  const handlePaste = useCallback((event) => {
    const items = event.clipboardData.items;
    for (const item of items) {
      if (item.type.indexOf("image") !== -1) {
        const file = item.getAsFile();
        const reader = new FileReader();
        reader.onload = (event) => {
          setPastedImage(event.target.result);
        };
        reader.readAsDataURL(file);
      }
    }
  }, []);
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
      if (e.ctrlKey && e.shiftKey && e.key === "X") {
        e.preventDefault();
        setPastedImage(null);
      }
    },
    [handleSubmit, setSearchData]
  );

  useEffect(() => {
    // Thêm sự kiện keydown vào document khi component mount
    document.addEventListener("keydown", handleKeyDown);
    document.addEventListener("paste", handlePaste);

    // Xóa sự kiện khi component unmount
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("paste", handlePaste);
    };
  }, [handleKeyDown, handlePaste]);

  return (
    <div className="search-interface">
      <div className="container">
        <div className="wrapper-raw-text-area">
          <Slider
            handleChangePriority={handleChangePriority}
            name="raw-text-priority"
          />
          <textarea
            name="rawText"
            id="raw-text"
            className="raw-text-area"
            placeholder="enter key search"
            onChange={handleChangeSearchData}
            value={searchData.rawText.value}
          />
        </div>
        <div className="wrapper-search-by-task-area">
          <Slider
            handleChangePriority={handleChangePriority}
            name="objects-priority"
          />
          <div className="task-item">
            <label htmlFor="objects" className="label-task">
              Objects
            </label>
            <input
              type="text"
              name="objects"
              id="objects"
              className="task-content"
              value={searchData.object}
              // onChange={handleChangeSearchData}
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
        </div>
        {/* <Datetime />/ */}
        <div className="button-block">
          <button className="search-button" onClick={handleSubmit}>
            Search
          </button>
          <button className="clear-button" onClick={resetSearchData}>
            Clear
          </button>
        </div>
        <Slider
          handleChangePriority={handleChangePriority}
          name="colors-priority"
        />
        <div className="color-zone" id="color-szone">
          <div className="content">
            <div
              className="image-data"
              contentEditable={true}
              suppressContentEditableWarning={true}
              onPaste={handlePaste}
              tabIndex={0}
            >
              {pastedImage ? (
                <img src={pastedImage} alt="Pasted content" />
              ) : null}
            </div>
            <ColorZone
              searchData={searchData}
              setSearchData={setSearchData}
              currentColor={currentColor}
            />
          </div>
        </div>

        <div className="wrapper-color-picker">
          <ColorPicker
            currentColor={currentColor}
            setCurrentColor={setCurrentColor}
          />
        </div>
      </div>
    </div>
  );
};

export default SearchInterface;

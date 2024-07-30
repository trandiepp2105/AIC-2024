import React, { useCallback, useEffect, useState, useRef } from "react";
import "./SearchInterface.scss";
import ColorPicker from "../ColorPicker/ColorPicker";
import { useHomeContext } from "../../pages/home-page/HomePage";
import ColorZone from "../ColorZone/ColorZone";
import Slider from "../Slider/Slider";
import ListClass from "../ListClass/ListClass";
import getClasses from "../../services/get_classes";
import fuzzySearch from "../../services/fuzzy_search";

const SearchInterface = () => {
  const [classes, setClasses] = useState([]);
  const [classesIndexDisplay, setClassesIndexDisplay] = useState([]);
  useEffect(() => {
    const fetchClasses = async () => {
      try {
        const response = await getClasses();
        if (response && response.status >= 200 && response.status < 300) {
          setClasses(response.data.result);
          setClassesIndexDisplay(
            Array.from({ length: response.data.result.length }, (_, i) => i)
          );

          console.log("Initial Classes Set:", response.data.result);
        } else {
          setClasses([]);
          setClassesIndexDisplay([]);
        }
      } catch (error) {
        console.error("Failed to fetch classes:", error);
        setClasses([]);
        setClassesIndexDisplay([]);
      }
    };

    fetchClasses();
  }, []);

  useEffect(() => {
    console.log("index: ", classesIndexDisplay);
  }, [classesIndexDisplay]);
  const [currentColor, setCurrentColor] = useState("#4093e6");
  const [pastedImage, setPastedImage] = useState(null);
  const [activeImageOption, setActiveImageOption] = useState("colors");
  const [showListClass, setShowListClass] = useState(false);
  const objectsInputRef = useRef(null);
  const listClassRef = useRef(null);
  const imageDataRef = useRef(null);

  const { searchData, setSearchData, initialSearchData, handleSearchText } =
    useHomeContext();

  const handleChangeSearchData = (e) => {
    const { name, value } = e.target;
    setSearchData((prevData) => ({
      ...prevData,
      [name]: {
        ...prevData[name],
        value: value,
      },
    }));
  };

  const handleChangePriority = (event) => {
    const { name, value } = event.target;
    const fieldName = convertText(name);
    setSearchData((prevData) => ({
      ...prevData,
      [fieldName]: {
        ...prevData[fieldName],
        priority: parseInt(value),
      },
    }));
  };

  const convertText = (text) => {
    const parts = text.split("-");
    const lastPart = parts.pop().replace("priority", "");
    const capitalizedParts = parts.map((part, index) =>
      index === 0 ? part : part.charAt(0).toUpperCase() + part.slice(1)
    );
    return capitalizedParts.join("") + lastPart;
  };

  const resetSearchData = () => {
    setSearchData(initialSearchData);
    setPastedImage(null);
    const fetchClasses = async () => {
      try {
        const response = await getClasses();
        if (response && response.status >= 200 && response.status < 300) {
          setClasses(response.data.result);
          console.log("Initial Classes Set:", response.data.result);
        } else {
          setClasses([]);
        }
      } catch (error) {
        console.error("Failed to fetch classes:", error);
        setClasses([]);
      }
    };

    fetchClasses();
  };

  const handleSubmit = useCallback(async () => {
    await handleSearchText(searchData);
    document.activeElement?.blur();
  }, [searchData, handleSearchText]);

  const handlePaste = useCallback(
    (event) => {
      const items = event.clipboardData.items;
      for (const item of items) {
        if (item.type.indexOf("image") !== -1) {
          const file = item.getAsFile();
          const reader = new FileReader();
          reader.onload = (event) => {
            const base64Image = event.target.result;
            setPastedImage(base64Image);
            setSearchData((prevData) => ({
              ...prevData,
              image: {
                ...prevData.image,
                value: base64Image,
              },
            }));
          };
          reader.readAsDataURL(file);
        }
      }
    },
    [setSearchData]
  );

  const handleDrop = useCallback(
    (event) => {
      event.preventDefault();
      const srcDrop = event.dataTransfer.getData("text/plain");
      setPastedImage(srcDrop);
      fetch(srcDrop)
        .then((response) => response.blob())
        .then((blob) => {
          const reader = new FileReader();
          reader.onload = (event) => {
            const base64Image = event.target.result;

            setSearchData((prevData) => ({
              ...prevData,
              image: {
                ...prevData.image,
                value: base64Image,
              },
            }));
          };
          reader.readAsDataURL(blob);
        })
        .catch((error) => {
          console.error("Error fetching image:", error);
        });
    },
    [setSearchData]
  );

  const handleDragOver = useCallback((event) => {
    event.preventDefault();
  }, []);

  const handleKeyDown = useCallback(
    (e) => {
      const focusedElement = document.activeElement;
      const isInputOrTextarea =
        focusedElement.tagName === "TEXTAREA" ||
        focusedElement.tagName === "INPUT";

      if (e.key === "Enter") {
        if (e.shiftKey) {
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

  const handleChangeActiveImageOption = (option) => {
    setActiveImageOption(option);
  };

  const handleOutsideClick = (event) => {
    if (
      objectsInputRef.current &&
      !objectsInputRef.current.contains(event.target) &&
      listClassRef.current &&
      !listClassRef.current.contains(event.target) &&
      document.activeElement !== objectsInputRef.current // Kiểm tra con trỏ nhập
    ) {
      setShowListClass(false);
    }
  };

  const handleSearchObjects = (event) => {
    event.preventDefault();
    const value = event.target.value;
    const filterIndex = fuzzySearch(value, classes);
    setClassesIndexDisplay(filterIndex);
    console.log("filter: ", filterIndex);
  };

  useEffect(() => {
    document.addEventListener("keydown", handleKeyDown);
    document.addEventListener("paste", handlePaste);
    document.addEventListener("click", handleOutsideClick);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("paste", handlePaste);
      document.removeEventListener("click", handleOutsideClick);
    };
  }, [handleKeyDown, handlePaste]);

  return (
    <div className="search-interface">
      <div className="container">
        <div className="wrapper-raw-text-area">
          <Slider
            handleChangePriority={handleChangePriority}
            name="raw-text-priority"
            initValue={searchData.rawText.priority}
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
            initValue={searchData.objects.priority}
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
              onFocus={() => setShowListClass(true)}
              ref={objectsInputRef}
              onChange={handleSearchObjects}
            />
            {showListClass && (
              <div className="wrapper-list-class" ref={listClassRef}>
                <ListClass
                  classes={classes}
                  setClasses={setClasses}
                  searchData={searchData}
                  setSearchData={setSearchData}
                  classesIndexDisplay={classesIndexDisplay}
                  setClassesIndexDisplay={setClassesIndexDisplay}
                />
              </div>
            )}
          </div>
          <Slider
            handleChangePriority={handleChangePriority}
            name="time-priority"
            initValue={searchData.time.priority}
          />
          <div className="task-item">
            <label htmlFor="time" className="label-task">
              Time
            </label>
            <input
              type="text"
              name="time"
              id="time"
              className="task-content"
              value={searchData.time.value}
              onChange={handleChangeSearchData}
            />
          </div>
          <Slider
            handleChangePriority={handleChangePriority}
            name="ocr-priority"
            initValue={searchData.ocr.priority}
          />
          <div className="task-item">
            <label htmlFor="ocr" className="label-task">
              OCR
            </label>
            <input
              type="text"
              name="ocr"
              id="ocr"
              className="task-content"
              value={searchData.ocr.value}
              onChange={handleChangeSearchData}
            />
          </div>
          <Slider
            handleChangePriority={handleChangePriority}
            name="speech-priority"
            initValue={searchData.speech.priority}
          />
          <div className="task-item">
            <label htmlFor="speech" className="label-task">
              Speech
            </label>
            <input
              type="text"
              name="speech"
              id="speech"
              className="task-content"
              value={searchData.speech.value}
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
        <Slider
          handleChangePriority={handleChangePriority}
          name={`${activeImageOption}-priority`}
          initValue={searchData[activeImageOption].priority}
        />
        <div className="color-zone" id="color-zone">
          <div className="color-zone-option">
            <button
              className={`colors-table-opt ${
                activeImageOption === "colors" ? "active-opt" : ""
              }`}
              onClick={() => handleChangeActiveImageOption("colors")}
            >
              COLORS PICK
            </button>
            <button
              className={`image-opt ${
                activeImageOption === "image" ? "active-opt" : ""
              }`}
              onClick={() => handleChangeActiveImageOption("image")}
            >
              IMAGE
            </button>
          </div>
          <div className="content">
            {activeImageOption === "image" ? (
              <div
                className="image-data"
                // contentEditable={true}
                // suppressContentEditableWarning={true}
                onPaste={handlePaste}
                ref={imageDataRef}
                // tabIndex={0}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
              >
                {pastedImage && <img src={pastedImage} alt="Pasted content" />}
              </div>
            ) : (
              <ColorZone
                searchData={searchData}
                setSearchData={setSearchData}
                currentColor={currentColor}
              />
            )}
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

import React, {
  useCallback,
  useEffect,
  useState,
  useRef,
  useContext,
} from "react";
import "./SearchInterface.scss";
import ColorPicker from "../ColorPicker/ColorPicker";
import { useHomeContext } from "../../pages/home-page/HomePage";
import ColorZone from "../ColorZone/ColorZone";
import Slider from "../Slider/Slider";
import ListClass from "../ListClass/ListClass";
import getClasses from "../../services/get_classes";
import fuzzySearch from "../../services/fuzzy_search";
import translate from "../../services/translate";
const SearchInterface = ({ currentTranslateKey }) => {
  useEffect(() => {
    console.log("Component mounted");
    // Code chỉ chạy khi component mount
  }, []);
  const [classes, setClasses] = useState([]);
  const [classesIndexDisplay, setClassesIndexDisplay] = useState([]);
  const rawTextAreaRef = useRef([]); // Tạo ref cho textarea
  useEffect(() => {
    // const fetchClasses = async () => {
    //   try {
    //     const response = await getClasses();
    //     if (response && response.status >= 200 && response.status < 300) {
    //       setClasses(response.data.result);
    //       setClassesIndexDisplay(
    //         Array.from({ length: response.data.result.length }, (_, i) => i)
    //       );
    //       console.log("Initial Classes Set:", response.data.result);
    //     } else {
    //       setClasses([]);
    //       setClassesIndexDisplay([]);
    //     }
    //   } catch (error) {
    //     console.error("Failed to fetch classes:", error);
    //     setClasses([]);
    //     setClassesIndexDisplay([]);
    //   }
    // };
    // fetchClasses();
  }, []);

  useEffect(() => {
    console.log("index: ", classesIndexDisplay);
  }, [classesIndexDisplay]);
  const [currentColor, setCurrentColor] = useState("#4093e6");
  const [pastedImage, setPastedImage] = useState(null);
  const [activeImageOption, setActiveImageOption] = useState("image");
  const [showListClass, setShowListClass] = useState(false);
  const objectsInputRef = useRef(null);
  const listClassRef = useRef(null);
  const imageDataRef = useRef(null);

  const {
    searchData,
    setSearchData,
    initialSearchData,
    handleSearchText,
    handleQueryIndexChange,
    queryIndex,
    queryMode,
    checkMode,
    searchType,
    checkSearchType,
    setBrowsingOption,
    rawTextQuantity,
    setRawTextQuantity,
  } = useHomeContext();
  const listBrowsingOption = {
    browsing: "browsing",
    picked: "picked",
    teamPicked: "team-picked",
  };
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
    setRawTextQuantity(1);
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
    setBrowsingOption(listBrowsingOption.browsing);
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
    (e, index) => {
      const focusedElement = document.activeElement;

      if (e.key === "Enter") {
        e.preventDefault();
        if (e.shiftKey) {
          if (focusedElement.tagName === "TEXTAREA") {
            const cursorPosition = focusedElement.selectionStart;
            const value = focusedElement.value;

            // Thêm dòng mới tại vị trí con trỏ trong TEXTAREA hiện tại
            focusedElement.value =
              value.substring(0, cursorPosition) +
              "\n" +
              value.substring(cursorPosition);
            focusedElement.selectionStart = cursorPosition + 1;
            focusedElement.selectionEnd = cursorPosition + 1;

            // Cập nhật rawText là mảng các chuỗi, thay đổi giá trị tại index
            setSearchData((prevData) => {
              const updatedRawTextValue = [...prevData.rawText.value]; // Tạo bản sao của rawText
              updatedRawTextValue[index] = focusedElement.value; // Cập nhật phần tử tại index

              return {
                ...prevData,
                rawText: {
                  ...prevData.rawText,
                  value: updatedRawTextValue,
                }, // Gán lại rawText với mảng đã cập nhật
              };
            });
          }
        } else {
          handleSubmit(); // Gửi dữ liệu nếu chỉ nhấn Enter mà không giữ Shift
        }
      }

      // Xử lý tổ hợp Ctrl + Shift + X
      if (e.ctrlKey && e.shiftKey && e.key === "X") {
        e.preventDefault();
        setPastedImage(null); // Xóa ảnh đã dán
      }

      if (e.shiftKey && e.key === "E") {
        e.preventDefault();
        // Thêm logic xử lý khi nhấn Shift + E ở đây
        console.log("Shift + E pressed");
        isCurrentFrameTranslating.forEach(async (_, index) => {
          await handleTranslate(
            index,
            translateLanguague.vi,
            translateLanguague.en
          );
        });
      }

      // Xử lý tổ hợp Shift + V
      if (e.shiftKey && e.key === "V") {
        e.preventDefault();
        // Thêm logic xử lý khi nhấn Shift + V ở đây
        isCurrentFrameTranslating.forEach(async (_, index) => {
          await handleTranslate(
            index,
            translateLanguague.en,
            translateLanguague.vi
          );
        });
        console.log("Shift + V pressed");
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
    // const rawTextArea = rawTextAreaRef.current; // Lấy tham chiếu đến textarea
    // const nextFrameTextArea = nextFrameTextAreaRef.current;

    // if (rawTextArea) {
    //   rawTextArea.addEventListener("keydown", handleKeyDown); // Thêm sự kiện keydown cho textarea
    // }
    // if (nextFrameTextArea) {
    //   nextFrameTextArea.addEventListener("keydown", handleKeyDown);
    // }
    const popup = document.querySelector(".qa-input");
    // const rawTextArea = rawTextAreaRef.current;

    if (popup) {
      // Nếu popup có chỉ số z-index cao hơn thì không xử lý sự kiện
      console.log("popup");
      return;
    }
    document.addEventListener("paste", handlePaste);
    document.addEventListener("click", handleOutsideClick);
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      // if (rawTextArea) {
      //   rawTextArea.removeEventListener("keydown", handleKeyDown); // Xóa sự kiện khi component bị hủy
      // }
      // if (nextFrameTextArea) {
      //   nextFrameTextArea.removeEventListener("keydown", handleKeyDown); // Xóa sự kiện khi component bị hủy
      // }

      document.removeEventListener("paste", handlePaste);
      document.removeEventListener("click", handleOutsideClick);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [handleKeyDown, handlePaste]);
  const [isCurrentFrameTranslating, setIsCurrentFrameTranslating] = useState([
    {
      vi: false,
      en: false,
    },
  ]);

  const translateLanguague = {
    vi: "vi",
    en: "en",
  };

  const handleTranslate = async (rawTextIndex, from, to) => {
    // const rawTextArea = rawTextAreaRef.current; // Lấy tham chiếu đến textarea
    const rawTextArea = rawTextAreaRef.current[rawTextIndex]; // Lấy textarea hiện tại dựa trên index
    console.log("Start translate");
    try {
      const text = rawTextArea.value;
      if (text && text.trim() !== "") {
        setIsCurrentFrameTranslating((prevData) => {
          const prevDataArr = [...prevData];
          prevDataArr[rawTextIndex][from] = false;
          prevDataArr[rawTextIndex][to] = true;
          return prevDataArr;
        });
        const res = await translate(text, currentTranslateKey, from, to);
        if (res && res.status >= 200 && res.status < 300) {
          console.log(res.data.translation);
          rawTextArea.value = res.data.translation;
          setSearchData((prevData) => ({
            ...prevData,
            rawText: {
              ...prevData.rawText,
              value: Array.isArray(prevData.rawText.value)
                ? prevData.rawText.value.map((v, i) =>
                    i === rawTextIndex ? res.data.translation : v
                  )
                : [res.data.translation], // Nếu không phải là mảng, khởi tạo lại thành mảng mới với value
            },
          }));
        } else {
          console.log(res);
        }
      }
    } catch (error) {
      console.error("Translation failed:", error);
    } finally {
      setIsCurrentFrameTranslating((prevData) => {
        const prevDataArr = [...prevData];
        prevDataArr[rawTextIndex][from] = false;
        prevDataArr[rawTextIndex][to] = false;
        return prevDataArr;
      });
    }
  };
  return (
    <div className="search-interface">
      <div className="container">
        <div className="place-query-index">
          <div>
            <label htmlFor="query-index-input">Index: </label>
            <input
              type="number"
              id="query-index-input"
              className="query-index-input"
              onChange={(event) => handleQueryIndexChange(event)}
              value={queryIndex}
            />
          </div>
          <div className="query-mode">
            <div class="switch">
              <input
                type="checkbox"
                name="search-type"
                id="search-type"
                className="input"
                checked={searchType === "GRID"}
                onChange={checkSearchType}
              />
              <span class="slider"></span>
              <p className="QA-mode">Grid</p>
              <p className="text-mode">Array</p>
            </div>
          </div>
          <div className="query-mode">
            <div class="switch">
              <input
                type="checkbox"
                name="mode"
                id="mode"
                className="input"
                checked={queryMode === "QA"}
                onChange={checkMode}
              />
              <span class="slider"></span>
              <p className="QA-mode">Q&A</p>
              <p className="text-mode">TEXT</p>
            </div>
          </div>
        </div>

        {/* <Slider
          handleChangePriority={handleChangePriority}
          name="raw-text-priority"
          initValue={searchData.rawText.priority}
        /> */}
        {Array.from({ length: rawTextQuantity }, (_, index) => {
          return (
            <>
              <div className="picker-button-option current-frame-trans">
                <button>CURRENT FRAME</button>
                <div className="group-translate-btn">
                  <button
                    className={`translate-btn ${
                      isCurrentFrameTranslating[index].vi
                        ? "is-translating"
                        : null
                    }`}
                    onClick={() => {
                      handleTranslate(
                        index,
                        translateLanguague.en,
                        translateLanguague.vi
                      );
                    }}
                  >
                    VI
                  </button>
                  <button
                    className={`translate-btn ${
                      isCurrentFrameTranslating[index].en
                        ? "is-translating"
                        : null
                    }`}
                    onClick={() => {
                      handleTranslate(
                        index,
                        translateLanguague.vi,
                        translateLanguague.en
                      );
                    }}
                  >
                    EN
                  </button>
                </div>
              </div>
              <div className="raw-text-item" key={index}>
                <div className="wrapper-raw-text-area">
                  <textarea
                    name="rawText"
                    id={`raw-text-${index}`} // Đặt id duy nhất cho mỗi textarea
                    className="raw-text-area"
                    placeholder="enter key search"
                    onChange={(e) => {
                      const { name, value } = e.target;
                      setSearchData((prevData) => ({
                        ...prevData,
                        rawText: {
                          ...prevData.rawText,
                          value: Array.isArray(prevData.rawText.value)
                            ? prevData.rawText.value.map((v, i) =>
                                i === index ? value : v
                              )
                            : [value], // Nếu không phải là mảng, khởi tạo lại thành mảng mới với value
                        },
                      }));
                    }}
                    value={
                      Array.isArray(searchData.rawText.value)
                        ? searchData.rawText.value[index] || ""
                        : ""
                    }
                    ref={(el) => (rawTextAreaRef.current[index] = el)}
                  />
                </div>

                <div className="wrapper-add-raw-text-area">
                  <button
                    className="add-raw-text-btn"
                    onClick={(event) => {
                      event.stopPropagation();
                      setRawTextQuantity(rawTextQuantity + 1);
                      setSearchData((prevData) => ({
                        ...prevData,
                        rawText: {
                          ...prevData.rawText,
                          value: [...(prevData.rawText.value || []), ""], // Thêm một giá trị trống mới
                        },
                      }));

                      setIsCurrentFrameTranslating((prevState) => [
                        ...prevState, // Sao chép các phần tử hiện tại
                        { vi: false, en: false }, // Thêm phần tử mới
                      ]);
                    }}
                  >
                    ADD
                  </button>
                  {index !== 0 && ( // Chỉ hiển thị nút DELETE cho các mục không phải là mục đầu tiên
                    <button
                      className="delete-raw-text-btn"
                      onClick={(event) => {
                        event.stopPropagation();
                        setRawTextQuantity(rawTextQuantity - 1);
                        setSearchData((prevData) => ({
                          ...prevData,
                          rawText: {
                            ...prevData.rawText,
                            value: prevData.rawText.value.filter(
                              (_, i) => i !== index
                            ), // Xóa mục tại vị trí index
                          },
                        }));
                        setIsCurrentFrameTranslating(
                          (prevState) => prevState.filter((_, i) => i !== index) // Giữ lại các phần tử không phải là phần tử tại index
                        );
                      }}
                    >
                      DELETE
                    </button>
                  )}
                </div>
              </div>
            </>
          );
        })}

        <div className="wrapper-search-by-task-area">
          {/* ĐÂY LÀ SEARCH OBJECT */}
          {/* <Slider
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
          </div> */}
          {/* <Slider
            handleChangePriority={handleChangePriority}
            name="time-priority"
            initValue={searchData.time.priority}
          /> */}
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

          {/* ĐÂY LÀ SEARCH OCR */}
          {/* <Slider
            handleChangePriority={handleChangePriority}
            name="ocr-priority"
            initValue={searchData.ocr.priority}
          /> */}

          {/* <Slider
            handleChangePriority={handleChangePriority}
            name="speech-priority"
            initValue={searchData.speech.priority}
          /> */}
        </div>
        <div className="button-block">
          <button className="search-button" onClick={handleSubmit}>
            Search
          </button>
          <button className="clear-button" onClick={resetSearchData}>
            Clear
          </button>
        </div>
        {/* <Slider
          handleChangePriority={handleChangePriority}
          name={`${activeImageOption}-priority`}
          initValue={searchData[activeImageOption].priority}
        /> */}
        <div className="color-zone" id="color-zone">
          {/* <div className="picker-button-option color-zone-option">
            <button
              className={` ${
                activeImageOption === "colors" ? "actice-color-zone-btn" : ""
              }`}
              onClick={() => handleChangeActiveImageOption("colors")}
            >
              COLORS PICK
            </button>
            <button
              className={`${
                activeImageOption === "image" ? "actice-color-zone-btn" : ""
              }`}
              onClick={() => handleChangeActiveImageOption("image")}
            >
              IMAGE
            </button>
          </div> */}
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
            ) : null}
            {/* (
            <ColorZone
              searchData={searchData}
              setSearchData={setSearchData}
              currentColor={currentColor}
            />
            ) */}
          </div>
        </div>
        {/* <div className="wrapper-color-picker">
          <ColorPicker
            currentColor={currentColor}
            setCurrentColor={setCurrentColor}
          />
        </div> */}
        <span className="padding-box"> </span>
      </div>
    </div>
  );
};

export default SearchInterface;

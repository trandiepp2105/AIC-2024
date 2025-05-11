import React, {
  useState,
  createContext,
  useContext,
  useEffect,
  useRef,
} from "react";
import "./HomePage.scss";
import SearchInterface from "../../components/SearchInterface/SearchInterface";
import BrowsingInterface from "../../components/BrowsingInterface/BrowsingInterface";
import searchText from "../../services/search_text";
import getTeamPickedFrames from "../../services/get_team_picked";
import {
  NotificationContainer,
  // NotificationManager,
} from "react-notifications";
import "react-notifications/lib/notifications.css";
import download_all_query from "../../services/download_all_queries";
import Header from "../../components/Header/Header";
import SideBar from "../../components/SideBar/SideBar";
import deleteTeamPickedFrameByIndex from "../../services/delete_team_picked_by_index";
import { NotificationManager } from "react-notifications";
import "react-notifications/lib/notifications.css";
const HomePageContext = createContext();
const HomePage = () => {
  useEffect(() => {
    console.log("Component mounted");
    // Code chỉ chạy khi component mount
  }, []);
  const initialColorTable = {
    row: 6,
    column: 10,
  };

  initialColorTable.table = Array.from({ length: initialColorTable.row }, () =>
    Array.from({ length: initialColorTable.column }, () => "#fff")
  );

  const initialSearchData = {
    rawText: {
      priority: 10,
      value: [""],
    },
    nextFrameText: {
      priority: 10,
      value: "",
    },
    objects: {
      priority: 10,
      value: [],
    },
    time: {
      priority: 10,
      value: "",
    },
    colors: {
      priority: 10,
      value: initialColorTable,
    },
    image: {
      priority: 10,
      value: null,
    },
    ocr: {
      priority: 10,
      value: "",
    },
    speech: {
      priority: 10,
      value: "",
    },
  };
  const [searchData, setSearchData] = useState(initialSearchData);
  const [rawTextQuantity, setRawTextQuantity] = useState(1);
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pickedFrames, setPickedFrames] = useState([]);
  const [queryIndex, setQueryIndex] = useState(1);
  const [teamPickedFrames, setTeamPickedFrames] = useState([]);
  const [browsingOption, setBrowsingOption] = useState("browsing");
  // const confirmSubmit = async () => {
  //   const pickedFramesIndex = Array.from(pickedFrames);
  //   console.log(pickedFramesIndex);

  //   if (pickedFramesIndex.length > 0) {
  //     try {
  //       const results = await submitFrames(searchResults, pickedFramesIndex);

  //       // Kiểm tra xem kết quả trả về từ searchText có khác null không và có status thành công
  //       if (results && results.status >= 200 && results.status < 300) {
  //         setOnSubmit(false);
  //         NotificationManager.success("Submit successfully", "SUBMIT", 2000);
  //       } else {
  //         setOnSubmit(false);
  //         NotificationManager.error("Submit failed", "SUBMIT", 2000);
  //       }
  //     } catch (error) {
  //       console.error("Search failed:", error);
  //     }
  //   }
  // };

  const handleSearchText = async (searchData) => {
    setPickedFrames([]);
    setSearchResults([]);
    setLoading(true);
    console.log("search data: ", searchData);
    try {
      const results = await searchText(searchData, searchType);

      // Kiểm tra xem kết quả trả về từ searchText có khác null không và có status thành công
      if (results && results.status >= 200 && results.status < 300) {
        console.log("Search results:", results);
        setSearchResults(results.data.result); // Gán dữ liệu trả về cho searchResults
        setLoading(false);
      } else {
        console.log("No results or unsuccessful response");
        setSearchResults([]); // Gán giá trị rỗng nếu không có kết quả hoặc response không thành công
      }
      console.log("rel: ", results);
    } catch (error) {
      console.error("Search failed:", error);
      setSearchResults([]);
    }
  };

  useEffect(() => {
    console.log("search data from home: ", searchData);
  }, [searchData]);

  const [queryMode, setQueryMode] = useState("TEXT"); // Trạng thái checkbox
  const checkMode = () => {
    if (queryMode === "TEXT") {
      setQueryMode("QA");
    } else {
      setQueryMode("TEXT");
    }
  };

  const [searchType, setSearchType] = useState("GRID"); // Trạng thái checkbox
  const checkSearchType = () => {
    setSearchResults([]);
    if (searchType === "ARRAY") {
      setSearchType("GRID");
    } else {
      setSearchType("ARRAY");
    }
  };

  useEffect(() => {
    if (queryMode === "TEXT") {
      console.log("CHÊ ĐỘ TEXT ĐƯỢC BẬT!");
    } else {
      console.log("CHẾ ĐỘ Q&A ĐƯỢC BẬT!");
    }
  }, [queryMode]);

  useEffect(() => {
    if (searchType === "ARRAY") {
      console.log("CHÊ ĐỘ SEARCH ARRAY ĐƯỢC BẬT!");
    } else {
      console.log("CHẾ ĐỘ SEARCH GRID ĐƯỢC BẬT!");
    }
  }, [searchType]);

  useEffect(() => {
    console.log("Picked frames: ", pickedFrames);
  }, [pickedFrames]);

  // useEffect(() => {
  //   const handleClickOutside = (event) => {
  //     if (
  //       downloadConfirmRef.current &&
  //       !downloadConfirmRef.current.contains(event.target)
  //     ) {
  //       setIsDownloadConfirming(false);
  //     }
  //   };

  //   if (isDownloadConfirming) {
  //     document.addEventListener("click", handleClickOutside);
  //   } else {
  //     document.removeEventListener("click", handleClickOutside);
  //   }
  //   return () => {
  //     document.removeEventListener("click", handleClickOutside);
  //   };
  // }, [setIsDownloadConfirming, isDownloadConfirming]);

  const listTranslateKey = [
    "8d4d70c013msh26d434649fdf31cp117561jsndf9a75bd4a56",
    "1211f76bfdmshb51ca3220e9e3d1p14c796jsn8c98eafc655e",
    "f68094db65mshf1544ac4e5840c3p1a9a03jsnd4dff0c12adb",
  ];
  const [currentTranslateKey, setCurrentTranslateKey] = useState(
    listTranslateKey[0]
  );
  const handleQueryIndexChange = (event) => {
    const newValue = event.target.value;
    setQueryIndex(newValue);
  };

  const fetchTeamPickedFrames = async () => {
    const response = await getTeamPickedFrames(queryIndex, queryMode);
    if (response && response.status >= 200 && response.status < 300) {
      setTeamPickedFrames(response.data);
    } else {
      setTeamPickedFrames([]);
    }
  };
  const handleDeleteTeamPickedFrameByIndex = async (event, queryIndex) => {
    event.preventDefault();
    const response = await deleteTeamPickedFrameByIndex(queryIndex);
    if (response && response.status >= 200 && response.status < 300) {
      // Update team_picked_frames
      console.log("DELETE TEAM PICKED FRAME SUCCESS!");
      NotificationManager.success("Delete successfully", "DELETE", 3000);
      // Update team_picked_frames
      fetchTeamPickedFrames();
    }
  };

  return (
    <HomePageContext.Provider
      value={{
        searchData,
        setSearchData,
        initialSearchData,
        handleSearchText,
        handleQueryIndexChange,
        queryIndex,
        setQueryIndex,
        queryMode,
        setQueryMode,
        checkMode,
        searchType,
        checkSearchType,
        setTeamPickedFrames,
        browsingOption,
        setBrowsingOption,
        handleDeleteTeamPickedFrameByIndex,
        rawTextQuantity,
        setRawTextQuantity,
      }}
    >
      <Header />

      <div className="home-page">
        <NotificationContainer />

        <div className="container">
          {/* <SearchInterface currentTranslateKey={currentTranslateKey} /> */}
          <SideBar
            currentTranslateKey={currentTranslateKey}
            listTranslateKey={listTranslateKey}
            setCurrentTranslateKey={setCurrentTranslateKey}
          />
          <BrowsingInterface
            frameDisplay={searchResults}
            loading={loading}
            pickedFrames={pickedFrames}
            setPickedFrames={setPickedFrames}
            queryIndex={queryIndex}
            queryMode={queryMode}
            teamPickedFrames={teamPickedFrames}
            setTeamPickedFrames={setTeamPickedFrames}
            browsingOption={browsingOption}
            setBrowsingOption={setBrowsingOption}
            fetchTeamPickedFrames={fetchTeamPickedFrames}
            searchType={searchType}
          />
        </div>
      </div>
    </HomePageContext.Provider>
  );
};

export default HomePage;
export const useHomeContext = () => useContext(HomePageContext);

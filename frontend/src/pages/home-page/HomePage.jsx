import React, { useState, createContext, useContext, useEffect } from "react";
import "./HomePage.scss";
import SearchInterface from "../../components/SearchInterface/SearchInterface";
import BrowsingInterface from "../../components/BrowsingInterface/BrowsingInterface";
import searchText from "../../services/search_text";
const HomePageContext = createContext();
const HomePage = () => {
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
  };
  const [searchData, setSearchData] = useState(initialSearchData);
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const handleSearchText = async (searchData) => {
    setSearchResults([]);
    setLoading(true);
    console.log("search data: ", searchData);
    try {
      const results = await searchText(searchData);

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

  return (
    <HomePageContext.Provider
      value={{
        searchData,
        setSearchData,
        initialSearchData,
        handleSearchText,
      }}
    >
      <div className="home-page">
        <div className="container">
          <SearchInterface />
          <BrowsingInterface frameDisplay={searchResults} loading={loading} />
        </div>
      </div>
    </HomePageContext.Provider>
  );
};

export default HomePage;
export const useHomeContext = () => useContext(HomePageContext);

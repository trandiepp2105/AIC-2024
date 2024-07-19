import React, { useState, createContext, useContext } from "react";
import "./HomePage.scss";
import SearchInterface from "../../components/SearchInterface/SearchInterface";
import BrowsingInterface from "../../components/BrowsingInterface/BrowsingInterface";
import searchText from "../../services/search_text";
const HomePageContext = createContext();
const HomePage = () => {
  const initialSearchData = {
    rawText: "",
    object: "",
    quantity: 0,
    time: "",
    location: "",
    predicate: "",
    color: "",
  };
  const [searchData, setSearchData] = useState(initialSearchData);
  const [searchResults, setSearchResults] = useState([]);

  const handleSearchText = async (searchData) => {
    console.log("search data: ", searchData);
    try {
      const results = await searchText(searchData);

      // Kiểm tra xem kết quả trả về từ searchText có khác null không và có status thành công
      if (results && results.status >= 200 && results.status < 300) {
        console.log("Search results:", results);
        setSearchResults(results.data.result); // Gán dữ liệu trả về cho searchResults
      } else {
        console.log("No results or unsuccessful response");
        setSearchResults([]); // Gán giá trị rỗng nếu không có kết quả hoặc response không thành công
      }
      console.log("rel: ", results);
    } catch (error) {
      console.error("Search failed:", error);
      setSearchResults([]); // Gán giá trị rỗng trong trường hợp xảy ra lỗi
    }
  };

  return (
    <HomePageContext.Provider
      value={{ searchData, setSearchData, initialSearchData, handleSearchText }}
    >
      <div className="home-page">
        <div className="container">
          <SearchInterface />
          <BrowsingInterface frameDisplay={searchResults} />
        </div>
      </div>
    </HomePageContext.Provider>
  );
};

export default HomePage;
export const useHomeContext = () => useContext(HomePageContext);

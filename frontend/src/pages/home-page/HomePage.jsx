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
    try {
      const results = await searchText(searchData);
      console.log(results);
      setSearchResults(results);
    } catch (error) {
      console.error("Search failed:", error);
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

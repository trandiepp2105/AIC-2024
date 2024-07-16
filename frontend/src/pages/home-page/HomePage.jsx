import React, { useState, createContext, useContext } from "react";
import "./HomePage.scss";
import SearchInterface from "../../components/SearchInterface/SearchInterface";
import BrowsingInterface from "../../components/BrowsingInterface/BrowsingInterface";

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
  return (
    <HomePageContext.Provider
      value={{ searchData, setSearchData, initialSearchData }}
    >
      <div className="home-page">
        <div className="container">
          <SearchInterface />
          <BrowsingInterface />
        </div>
      </div>
    </HomePageContext.Provider>
  );
};

export default HomePage;
export const useSearchData = () => useContext(HomePageContext);

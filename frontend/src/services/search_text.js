import axios from "axios";
const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/search/`;
const searchText = async (searchData, searchType = "ARRAY") => {
  // Kiểm tra tất cả các trường trong searchData khác null và quantity khác 0
  // const allFieldsValid = Object.values(searchData).every(
  //   (value) => value !== null && value !== ""
  // );
  // const quantityValid =
  //   searchData.quantity !== null && searchData.quantity !== 0;
  const type = searchType.toLocaleLowerCase();
  const isSearchValid =
    searchData.rawText !== null && searchData.rawText !== "";
  if (isSearchValid) {
    try {
      const response = await axios.post(`${endpoint}${type}`, searchData, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      console.log("Search text successfully");
      return response;
    } catch (error) {
      console.error("Error occurred while searching text:", error);
      throw error;
    }
  } else {
    console.log("Validation failed. Not posting data.");
    // You may want to handle this case appropriately, e.g., show an error message
    return null;
  }
};

export default searchText;

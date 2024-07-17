import axios from "axios";
const endpoint = "http://127.0.0.1:8000/api/search/text";
const searchText = async (searchData) => {
  try {
    const response = await axios.post(endpoint, searchData, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("Search text successfully");
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default searchText;

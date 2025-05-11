import axios from "axios";
const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/classes`;
const getClasses = async () => {
  try {
    const response = await axios.get(endpoint, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("Get classes successfully");
    return response;
  } catch (error) {
    console.error("Error occurred while Get classes:", error);
    throw error;
  }
};

export default getClasses;

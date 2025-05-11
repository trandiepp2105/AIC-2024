import axios from "axios";
const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/login/`;
const getLoginInfor = async () => {
  try {
    const response = await axios.get(endpoint);
    const { data } = response;
    if (data) {
      localStorage.setItem("sessionID", data.sessionID);
      localStorage.setItem("evaluationID", data.evaluationID);
      console.log("GET LOGIN LOGIN INFOR SUCCESS!");
      return data;
    }

    console.log("GET LOGIN LOGIN INFOR FAILED!");
    return null;
  } catch (error) {
    console.error("ERROR OCCURRED WHILE GET LOGIN LOGIN INFOR:", error);
    throw error;
  }
};

export default getLoginInfor;

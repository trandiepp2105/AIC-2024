import axios from "axios";
const endpoint = `${process.env.REACT_APP_BACKEND_API_ENDPOINT}/login/`;
const loginUniqueInfor = async (loginInfor) => {
  console.log("endpoint: ", endpoint);
  try {
    const response = await axios.post(endpoint, loginInfor);
    console.log("LOGIN SUBMIT SYSTEM SUCCESS!");
    const { data } = response;
    if (data) {
      // login success
      return data;
    }
    return null;
  } catch (error) {
    console.error("ERROR OCCURRED WHILE LOGIN SUBMIT SYSTEM:", error);
    throw error;
  }
};

export default loginUniqueInfor;

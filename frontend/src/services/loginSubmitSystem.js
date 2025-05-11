import axios from "axios";
const endpointSessionId = `https://eventretrieval.one/api/v2/login`;
const evaluationEndpoint = `https://eventretrieval.one/api/v2/client/evaluation/list`;

const getSessionID = async (loginInfor) => {
  try {
    const response = await axios.post(`${endpointSessionId}`, loginInfor);
    console.log("GET SESSION ID SUCCESS!");
    if (response && response.data) {
      const sessionID = response.data.sessionId;
      // Lưu sessionID vào localStorage để không bị mất khi reload trang
      localStorage.setItem("sessionID", sessionID);

      return sessionID; // Trả về sessionID nếu tồn tại
    } else {
      console.error("Session ID not found in response data");
      return null;
    }
  } catch (error) {
    console.error("Error occurred while get session:", error);
    throw error;
  }
};

const getEvaluationId = async (sessionID) => {
  try {
    const response = await axios.get(evaluationEndpoint, {
      params: {
        session: sessionID,
      },
    });
    const { data } = response;
    console.log("evaluation data: ", data);
    if (data && data.id) {
      const evaluationID = data.id;
      console.log("Evaluation ID:", evaluationID);
      localStorage.setItem("evaluationID", evaluationID);

      return evaluationID; // Trả về evaluationId nếu tồn tại
    } else {
      console.error("Evaluation ID not found in response data");
      return null;
    }
  } catch (error) {
    console.error("Error occurred while getting evaluation ID:", error);
    throw error;
  }
};

const loginSubmitSystem = async (loginInfor) => {
  const sessionID = await getSessionID(loginInfor);
  if (sessionID) {
    const evaluationID = await getEvaluationId(sessionID);
    return {
      sessionID: sessionID,
      evaluationID: evaluationID,
    };
  } else {
    return null;
  }
};

export default loginSubmitSystem;

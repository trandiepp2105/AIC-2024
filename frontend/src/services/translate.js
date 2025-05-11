import axios from "axios";

const translate = async (
  query,
  key = "8d4d70c013msh26d434649fdf31cp117561jsndf9a75bd4a56",

  from = "vi",
  to = "en"
) => {
  const options = {
    method: "POST",
    url: "https://free-google-translator.p.rapidapi.com/external-api/free-google-translator",
    params: {
      from: from,
      to: to,
      query: query,
    },
    headers: {
      "x-rapidapi-key": key,
      "x-rapidapi-host": "free-google-translator.p.rapidapi.com",
      "Content-Type": "application/json",
    },
    data: {
      translate: "rapidapi",
    },
  };
  try {
    const response = await axios.request(options);
    return response;
  } catch (error) {
    throw error;
  }
};

export default translate;

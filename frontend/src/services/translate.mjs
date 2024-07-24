import axios from "axios";

const API_KEY = "AIzaSyCkkaEspebpIth1Z1eXf7oWl6wrYo8kcm4";
const API_URL = "https://translation.googleapis.com/language/translate/v2";

const translateText = async (text, targetLanguage = "en") => {
  const response = await axios.post(`${API_URL}?key=${API_KEY}`, {
    q: text,
    target: targetLanguage,
  });

  return response.data.data.translations[0].translatedText;
};

const text = translateText("chuối");
console.log(text);
// export default translateText;

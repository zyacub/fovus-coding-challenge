import axios from 'axios'
import App from '../App';

const { nanoid } = require("nanoid");


export const getPresignedUrl = async(API_ENDPOINT, filename, textInput) => {
    const encodedFilename = encodeURIComponent(filename);
    const encodedTextInput = encodeURIComponent(textInput);


    const url = `${API_ENDPOINT}?filename=${encodedFilename}&textInput=${encodedTextInput}`;

    console.log(url);
    const response = await axios({
        method: "GET",
        url: url
    });
    const presignedUrl = response.data.presignedUrl;
    console.log(presignedUrl);
    return presignedUrl;
};

export const fetchDatabaseContents = async (API_ENDPOINT) => {
  try {
      const response = await axios.get(API_ENDPOINT);
      return response.data;
  } catch (error) {
      console.error("Error fetching database contents:", error.message);
      throw error;
  }
};


export const uploadToPresignedUrl = async (presignedUrl, file, uploadProgress, setUploadProgress) => {
    const uploadResponse = await axios.put(presignedUrl, file, {
      headers: {
        "Content-Type": "application/input",
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        setUploadProgress(percentCompleted);
        console.log(`Upload Progress: ${percentCompleted}%`);
      },
    });
    console.log(uploadResponse);
};

export const saveToDatabase = async (API_ENDPOINT, inputText, inputFilePath) => {
    const id = nanoid();
    
    const encodedFilePath = encodeURIComponent(inputFilePath);
    const encodedTextInput = encodeURIComponent(inputText);
    const encodedID = encodeURIComponent(id);


    const url = `${API_ENDPOINT}?filepath=${encodedFilePath}&textInput=${encodedTextInput}&id=${encodedID}`;

    console.log(url);
    const response = await axios({
        method: "GET",
        url: url
    });
    return response.data;
};





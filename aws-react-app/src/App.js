import React, { useState, useEffect } from 'react';
import './App.css';
import { getPresignedUrl, uploadToPresignedUrl, saveToDatabase, fetchDatabaseContents } from './api/functions';

function App() {
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [inputDatabaseContents, setInputDatabaseContents] = useState([]);
  const [outputDatabaseContents, setOutputDatabaseContents] = useState([]);
  const [showInputDatabase, setShowInputDatabase] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);

  const API_UPLOAD_ENDPOINT = "https://cv5boncgdf.execute-api.us-east-1.amazonaws.com/fovusPreSignedUrlUpload";
  const DB_ENDPOINT = "https://cv5boncgdf.execute-api.us-east-1.amazonaws.com/fovusUploadToDB";
  const QUERYINPUT_DB_ENDPOINT = "https://cv5boncgdf.execute-api.us-east-1.amazonaws.com/fovusQueryInputDB";
  const QUERYOUTPUT_DB_ENDPOINT = "https://cv5boncgdf.execute-api.us-east-1.amazonaws.com/fovusQueryOutputDB";

  const fetchDatabaseData = async () => {
    setIsLoading(true);
    try {
      const inputData = await fetchDatabaseContents(QUERYINPUT_DB_ENDPOINT);
      const outputData = await fetchDatabaseContents(QUERYOUTPUT_DB_ENDPOINT);
      
      const flattenedInputData = inputData.flatMap(item => item);
      const flattenedOutputData = outputData.flatMap(item => item);
      
      setInputDatabaseContents(flattenedInputData);
      setOutputDatabaseContents(flattenedOutputData);
    } catch (error) {
      console.error("Error fetching database contents:", error.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDatabaseData();
  }, []);

  const handleTextChange = (e) => {
    setText(e.target.value);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Submitted:', { text, file });
    try {
      if (!file) {
        console.error("No file selected");
        return;
      }
      if (!text) {
        console.error("No text inputed");
        return;
      }
      const presignedUrl = await getPresignedUrl(API_UPLOAD_ENDPOINT, file.name, text);
      await uploadToPresignedUrl(presignedUrl, file, uploadProgress, setUploadProgress);
      console.log("FILE UPLOADED TO S3");
      const filePath = `fovus-coding-aws/${file.name}`;
      const dbResponse = await saveToDatabase(DB_ENDPOINT, text, filePath);
      console.log(dbResponse);
      
      setShowConfirmation(true);
      await fetchDatabaseData();
      
      setText('');
      setFile(null);
      setUploadProgress(0);
    } catch (error) {
      console.error("Error uploading file:", error.message);
    }
  };

  const toggleDatabase = () => {
    setShowInputDatabase(!showInputDatabase);
  };

  const handleRefresh = () => {
    fetchDatabaseData();
  };

  const closeConfirmation = () => {
    setShowConfirmation(false);
  };

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="textInput">Text Input:</label>
          <input
            type="text"
            id="textInput"
            value={text}
            onChange={handleTextChange}
            placeholder="Enter text here"
          />
        </div>
        <div className="form-group">
          <label htmlFor="fileInput">File Upload:</label>
          <input
            type="file"
            id="fileInput"
            onChange={handleFileChange}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      
      <div className="database-container">
        <div className="database-header">
          <h2>{showInputDatabase ? "Input Database Contents" : "Output Database Contents"}</h2>
          <div className="button-group">
            <button onClick={toggleDatabase} className="toggle-button">
              Switch to {showInputDatabase ? "Output" : "Input"} Database
            </button>
            <button onClick={handleRefresh} className="refresh-button" disabled={isLoading}>
              {isLoading ? "Refreshing..." : "Refresh Contents"}
            </button>
          </div>
        </div>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Path</th>
              {showInputDatabase && <th>Text Input</th>}
            </tr>
          </thead>
          <tbody>
            {(showInputDatabase ? inputDatabaseContents : outputDatabaseContents).map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.path}</td>
                {showInputDatabase && <td>{item.textInput}</td>}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showConfirmation && (
        <div className="modal">
          <div className="modal-content">
            <h2>File Submitted!</h2>
            <p>Your file has been successfully uploaded and saved to the database.</p>
            <button onClick={closeConfirmation}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

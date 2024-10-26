import React, { useState } from 'react';
import axios from 'axios';
import logo from './logo.svg'; // Assuming you want to use the existing logo for loading

const CsvUpload = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Replace with your backend endpoint for CSV processing
      const response = await axios.post('http://localhost:5000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResults(response.data); // Assuming response data contains the results
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="csv-upload-container">
      <h2>Upload CSV File</h2>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        Upload
      </button>

      {loading && (
        <div className="loading-indicator">
          <img src={logo} className="loading-logo" alt="Loading..." />
          <p>Loading, please wait...</p>
        </div>
      )}

      {results && (
        <div className="results-container">
          <h3>Results:</h3>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default CsvUpload;

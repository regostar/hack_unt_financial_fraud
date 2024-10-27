import React, { useState } from 'react';
import './UploadPage.css';
import Logo from './assets/logo.jpg'; 

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'text/csv' && selectedFile.size <= 10485760) { 
      setFile(selectedFile);
      setError('');
    } else {
      setError('Please upload a CSV file up to 10 MB.');
      setFile(null);
    }
  };

  const handleUpload = () => {
    if (!file) return;
    setUploading(true);
    setStatus(''); 
    setTimeout(() => {
      setUploading(false);
      // For testing, setting to always succeed
      setStatus('success');
    }, 3000);
  };

  return (
    <div className="upload-page halloween-theme">
      <header className="header">
        <img src={Logo} alt="Fraud Detection Logo" className="logo" />
        <h1>FraudDetection</h1>
      </header>

      <h2>Upload Your File</h2>
      <p>CSV files Up to 10 MB</p>
      <input type="file" onChange={handleFileChange} />
      {error && <p className="error">{error}</p>}
      
      {!uploading ? (
        <button onClick={handleUpload} disabled={!file || uploading}>
          Upload
        </button>
      ) : (
        <div className="loader-container">
          <div className="loader-bar">
            <div className="progress" />
            <div className="pumpkin">🎃</div>
          </div>
        </div>
      )}

      {status && (
        <div className={`status-bar ${status}`}>
          {status === 'success' ? 'Upload Successful!' : 'Upload Failed!'}
        </div>
      )}
    </div>
  );
};

export default UploadPage;
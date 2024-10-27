import React, { useState } from 'react';
import axios from 'axios';
import './UploadPage.css';
import Logo from './assets/logo.jpg';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState('');
  const [totalTransactions, setTotalTransactions] = useState(null);
  const [suspiciousTransactions, setSuspiciousTransactions] = useState(null);
  const [suspiciousTransactionsList, setSuspiciousTransactionsList] = useState([]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'text/csv' && selectedFile.size <= 20485760) {
      setFile(selectedFile);
      setError('');
    } else {
      setError('Please upload a CSV file up to 20 MB.');
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setStatus('');
    setTotalTransactions(null);
    setSuspiciousTransactions(null);
    setSuspiciousTransactionsList([]);
  
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      const response = await axios.post('https://5516pf0u5pcprx-8000.proxy.runpod.net/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        withCredentials: true
      });
      
      console.log(response.data);

      if (response.data) {
        setStatus('success');
        setTotalTransactions(response.data.total_transactions);
        setSuspiciousTransactions(response.data.suspicious_transactions_count);
        setSuspiciousTransactionsList(response.data.suspicious_transactions || []);
        alert("Upload completed");
      } else {
        throw new Error('Unexpected response format');
      }
    } catch (error) {
      console.error('Upload failed:', error);
      setStatus('error');
      setError(error.response?.data?.error || error.message || 'An error occurred during upload');
    } finally {
      setUploading(false);
    }
  };

  const getFraudProbabilityDisplay = (probability) => {
    if (probability > 0.345) {
      return { text: "Fraud Alert", color: "red" };
    } else if (probability >= 0.30) {
      return { text: "Less Probability", color: "yellow" };
    } else {
      return { text: "Low Probability", color: "green" };
    }
  };

  return (
    <div className="upload-page halloween-theme">
      <header className="header">
        <img src={Logo} alt="Fraud Detection Logo" className="logo" />
        <h1>FraudFolio</h1>
      </header>

      <h2>Upload Your File</h2>
      <p>CSV files Up to 20 MB</p>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      {error && <p className="error">{error}</p>}
      
      <button onClick={handleUpload} disabled={!file || uploading}>
        {uploading ? 'Uploading...' : 'Upload'}
      </button>

      {uploading && (
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

      {totalTransactions !== null && suspiciousTransactions !== null && (
        <div className="transaction-info">
          <p>Total transactions: {totalTransactions}</p>
          <p>Suspicious transactions: {suspiciousTransactions}</p>
        </div>
      )}

      {suspiciousTransactionsList.length > 0 && (
        <div className="suspicious-transactions-table">
          <h3>Suspicious Transactions</h3>
          <table>
            <thead>
              <tr>
                <th>Transaction ID</th>
                <th>Cardholder Name</th>
                <th>Device</th>
                <th>Fraud Probability</th>
              </tr>
            </thead>
            <tbody>
              {suspiciousTransactionsList.map((transaction) => {
                const fraudProbability = getFraudProbabilityDisplay(transaction.Fraud_Probability);
                return (
                  <tr key={transaction['Transaction ID']}>
                    <td>{transaction['Transaction ID']}</td>  
                    <td>{transaction['Name']}</td>
                    <td>{transaction['Device']}</td>
                    <td style={{ color: fraudProbability.color }}>
                      {fraudProbability.text}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default UploadPage;
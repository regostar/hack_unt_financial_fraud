import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import LandingPage from './landingpage';
import Login from './Login';
import UploadPage from './UploadPage'; 

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/Landingpage" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/upload" element={<UploadPage />} /> 
        </Routes>
      </div>
    </Router>
  );
}

export default App;
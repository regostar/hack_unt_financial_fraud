import React, { useState } from 'react';
import './login.css'; 
import Logo from './assets/logo.jpg';
import ChartImage from './assets/chart-image.jpg';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log("Form submitted with:", { email, password });
    } catch (error) {
      setError('Invalid email or password.');
    }
  };

  return (
    <div className="login-page">
      <div className="logo-container">
        <img src={Logo} alt="Fraud Detection Logo" className="logo" />
        <h1>FraudFolio</h1>
      </div>

      <div className="login-left">
        <form onSubmit={handleSubmit} className="login-form">
          <div className="signup-link">
            Don’t have an account? <a href="/signup">Sign up</a>
          </div>
          
          <h2>Sign in</h2>
          {error && <p className="error">{error}</p>}
          
          <div className="input-group">
            <label>Email</label>
            <input
              type="email"
              placeholder="example.email@gmail.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter at least 8+ characters"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="login-options">
            <label>
              <input type="checkbox" /> Remember me
            </label>
            <a href="/forgot-password" className="forgot-password">Forgot password?</a>
          </div>

          <button type="submit" className="login-button">Sign in</button>

          <div className="social-login">
            <p>Or sign in with</p>
            <div className="social-icons">
              <button className="social-button google">G</button>
              <button className="social-button facebook">F</button>
              <button className="social-button apple">A</button>
            </div>
          </div>
        </form>
      </div>

      <div className="login-right">
        <div className="info-section">
          <div className="chart-placeholder">
            <img src={ChartImage} alt="Chart" className="chart-image" />
          </div>
          <h3>Detecting Threats, Protecting Trust</h3>
        </div>
      </div>
    </div>
  );
};

export default Login;

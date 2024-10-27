import React from "react";
import Logo from "./assets/logo.jpg"; 
import MockupImage from "./assets/mockup.jpg"; 
import "./landingpage.css";

const LandingPage = () => {
    return (
      <div className="landing-page">
        <header className="header">
          <img src={Logo} alt="Fraud Detection Logo" className="logo" />
          <h1>FraudFolio</h1>
        </header>
  
        <div className="text-content">
          <h2>About Us</h2>
          <p>Got transactions? Let's give them a quick once-over for any sneaky fraudsters!</p>
          <button className="cta-button">Go ahead, and try it out</button>
      </div>

      <div className="image-content">
        <img src={MockupImage} alt="Credit Card Mockup" className="mockup-image" />
      </div>
    </div>
  );
};

export default LandingPage;

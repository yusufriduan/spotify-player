import "../App.css";
import React, { useState, useEffect } from "react";

const Header: React.FC = () => {
  const getGreeting = () => {
    const currentHour = new Date().getHours();
    if (currentHour < 12) {
      return "Good morning";
    } else if (currentHour < 18) {
      return "Good afternoon";
    } else if (currentHour < 21) {
      return "Good evening";
    } else {
      return "Good night";
    }
  };
  const [greeting, setGreeting] = useState(getGreeting());

  useEffect(() => {
    const interval = setInterval(() => {
      setGreeting(getGreeting());
    }, 60000); // Update every minute

    return () => clearInterval(interval); // Cleanup interval on component unmount
  }, []);

  return (
    <header>
      <div className="userinfo">
        <h1>Hello,</h1>
      </div>
      <h2>{greeting}!</h2>
    </header>
  );
};

export default Header;

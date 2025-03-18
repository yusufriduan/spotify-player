import "../App.css";
import React, { useState, useEffect } from "react";
import LogoutButton from "./LogoutButton";

const Header: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const userName = localStorage.getItem("userName") || "Guest";

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

  useEffect(() => {
    const access_token = localStorage.getItem("access_token");
    if (access_token) {
      setIsLoggedIn(true);
    } else {
      setIsLoggedIn(false);
    }
  }, []);

  return (
    <header>
      <div className="userinfo">
        <h1>Hello, {userName}</h1>
        <h2>{greeting}!</h2>
      </div>
      {isLoggedIn && <LogoutButton />}
    </header>
  );
};

export default Header;
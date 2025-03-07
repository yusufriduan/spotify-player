import React from "react";
import "./App.css";
import Clock from "./components/clock.tsx";
import Date from "./components/date.tsx";
import Header from "./components/header.tsx";
import Player from "./components/player.tsx";
import backgroundImage from "./assets/1531.png";

const App: React.FC = () => {
  return (
    <div className="App">
      <header className="App-header">
        <Header />
      </header>
      <main>
        <Date />
        <Clock />
        <img src={backgroundImage} alt="Background" className="backgroundImg" />
        <Player />
      </main>
    </div>
  );
};

export default App;

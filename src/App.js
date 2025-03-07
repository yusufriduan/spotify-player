import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const handlePlay = async () => {
    try {
      await axios.get("http://localhost:5000/play");
    } catch (error) {
      console.error("Error playing the song", error);
    }
  };

  const handlePause = async () => {
    try {
      await axios.get("http://localhost:5000/pause");
    } catch (error) {
      console.error("Error pausing the song", error);
    }
  };

  const [playbackState, setPlaybackState] = useState(null);
  useEffect(() => {
    fetch("/api/playback-state")
      .then((response) => response.json())
      .then((data) => setPlaybackState(data));
  }, []);

  return (
    <div className="App">
      {playbackState ? (
        <>
          <div className="TrackInfo">
            <h1>Now Playing: {playbackState.item.name}</h1>
            <p>Artist: {playbackState.item.artists[0].name}</p>
          </div>
          <div className="Controls">
            <button onClick={handlePlay}>Play</button>
            <button onClick={handlePause}>Pause</button>
          </div>
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;

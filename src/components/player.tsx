import { useState, useEffect } from "react";
import axios from "axios";
import "../App.css";
import spotifyButton from "./button.tsx";

interface PlaybackState {
  item: {
    name: string;
    artists: { name: string }[];
  };
}

function player() {
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

  const [playbackState, setPlaybackState] = useState<PlaybackState | null>(null);
  useEffect(() => {
    axios
      .get("http://localhost:5000/currentPlaying")
      .then((response) => setPlaybackState(response.data))
      .catch((error) => console.error("Error fetching playback state", error));
  }, []);

  return (
    <div className="player">
      {playbackState ? (
        <>
          <div className="TrackInfo">
            <h2>{playbackState?.item?.name}</h2>
            <h3>{playbackState?.item?.artists[0]?.name}</h3>
          </div>
          <div className="playerControls">
            <button onClick={handlePlay}>Play</button>
            <button onClick={handlePause}>Pause</button>
          </div>
        </>
      ) : (
        <div style={{ textAlign: "center", alignSelf: "center" }}>
          <h3>You're not logged in</h3>
          {spotifyButton()}
        </div>
      )}
    </div>
  );
}

export default player;
import { useState, useEffect } from "react";
import axios from "axios";
import "../App.css";
import spotifyButton from "./LoginButton.tsx";

interface PlaybackState {
  item: {
    name: string;
    artists: { name: string }[];
  };
}

function player() {
  const [playbackState, setPlaybackState] = useState<PlaybackState | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  useEffect(() => {
    const access_token = localStorage.getItem("access_token");
    if (access_token) {
      setIsLoggedIn(true);
      axios
      .get("http://localhost:5000/currentPlaying", {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      })
      .then((response) => setPlaybackState(response.data))
      .catch((error) => console.error("Error fetching playback state", error));
    } else {
      setIsLoggedIn(false);
    }
  }, []);

  const handlePlay = async () => {
    try {
      await axios.get("http://localhost:5000/play", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });
    } catch (error) {
      console.error("Error playing the song", error);
    }
  };

  const handlePause = async () => {
    try {
      await axios.get("http://localhost:5000/pause", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });
    } catch (error) {
      console.error("Error pausing the song", error);
    }
  };

  return (
    <div className="player">
      {isLoggedIn ? (
        <>
          <div className="TrackInfo">
            <h2>{playbackState?.item?.name}</h2>
            <h3>{playbackState?.item?.artists[0]?.name}</h3>
          </div>
          <div className="playerControls">
            <button onClick={handlePlay}>▶</button>
            <button onClick={handlePause}>⏸</button>
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
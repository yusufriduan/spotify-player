import { useState, useEffect } from "react";
import axios from "axios";
import "../App.css";
import spotifyButton from "./LoginButton.tsx";

interface PlaybackState {
  item: {
    name: string;
    artists: { name: string }[];
    duration_ms: number;
  };
  progress_ms: number;
  is_playing: boolean;
}

function Player() {
  const [playbackState, setPlaybackState] = useState<PlaybackState | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [progress, setProgress] = useState<number>(0);

  useEffect(() => {
    const access_token = sessionStorage.getItem("access_token");
    if (access_token) {
      setIsLoggedIn(true);
      fetchCurrentPlaying(access_token);
      const interval = setInterval(() => {
        fetchCurrentPlaying(access_token);
      }, 1000);

      return () => clearInterval(interval);
    } else {
      setIsLoggedIn(false);
    }
  }, []);

  const fetchCurrentPlaying = (access_token: string) => {
    axios.get("http://localhost:5000/currentPlaying", {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      })
      .then((response) => {
        setPlaybackState(response.data);
        setProgress(response.data.progress_ms);
      })
      .catch((error) => console.error("Error fetching playback state", error));
  };

  useEffect(() => {
    let interval: ReturnType<typeof setInterval> | null = null;
    if (playbackState?.is_playing) {
      interval = setInterval(() => {
        setProgress((prevProgress) => prevProgress + 1000);
      }, 1000);
    } else if (interval) {
      clearInterval(interval);
    }
    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [playbackState?.is_playing]);

  const handlePlay = async () => {
    try {
      await axios.get("http://localhost:5000/play", {
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem("access_token")}`,
        },
      });
      setPlaybackState((prevState) => prevState && { ...prevState, is_playing: true });
    } catch (error) {
      console.error("Error playing the song", error);
    }
  };

  const handlePause = async () => {
    try {
      await axios.get("http://localhost:5000/pause", {
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem("access_token")}`,
        },
      });
      setPlaybackState((prevState) => prevState && { ...prevState, is_playing: false });
    } catch (error) {
      console.error("Error pausing the song", error);
    }
  };

  const getProgressPercentage = () => {
    if (playbackState) {
      return (progress / playbackState.item.duration_ms) * 100;
    }
    return 0;
  };

  return (
    <div className="player">
      {isLoggedIn ? (
        <>
          <div className="TrackInfo">
            <h2>{playbackState?.item?.name}</h2>
            <h3>{playbackState?.item?.artists[0]?.name}</h3>
          </div>
          <div className="progressBar">
            <div
              className="progress"
              style={{ width: `${getProgressPercentage()}%` }}
            ></div>
          </div>
          <div className="playerControls">
            <button onClick={handlePlay} className="playButton">⏵︎</button>
            <button onClick={handlePause} className="pauseButton">⏸︎</button>
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

export default Player;
import "../App.css";

function spotifyButton() {
  const sendDataToBackend = async () => {
    try {
      const response = await fetch("http://localhost:5000/login", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data["url"]);
        window.location.href = data["url"];
      }
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <div className="spotifyButton">
      <button onClick={sendDataToBackend}>Login with Spotify</button>
    </div>
  );
}

export default spotifyButton;
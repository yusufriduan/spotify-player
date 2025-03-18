import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Callback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const access_token = params.get("access_token");
    const refresh_token = params.get("refresh_token");
    const expires_in = params.get("expires_in");
    const userId = params.get("user_id");
    const userName = params.get("user_name");

    if (access_token && refresh_token && expires_in && userId && userName) {
      sessionStorage.setItem("access_token", access_token);
      sessionStorage.setItem("refresh_token", refresh_token);
      sessionStorage.setItem("expires_in", expires_in);
      sessionStorage.setItem("userId", userId);
      sessionStorage.setItem("userName", userName);
      navigate("/");
    } else {
        navigate("/");
        console.error("Missing user details");
    }
  }, [navigate]);

  return <div>Redirecting...</div>;
};

export default Callback;
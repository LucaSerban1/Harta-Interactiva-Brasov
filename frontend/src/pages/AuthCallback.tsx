import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function AuthCallback() {
  const navigate = useNavigate();
  useEffect(() => {
    const token = new URLSearchParams(window.location.search).get("token");
    if (token) {
      localStorage.setItem("token", token);
      navigate("/profile");
    }
  }, []);
  return <div style={{ padding: '2rem' }}>Se autentifică...</div>;
}
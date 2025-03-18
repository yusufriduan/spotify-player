import { createRoot } from "react-dom/client";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import App from "./app.tsx";
import Callback from "./callback.tsx";

createRoot(document.getElementById("root")!).render(
  <Router>
    <Routes>
      <Route path="/" element={<App />}></Route>
      <Route path="/callback" element={<Callback />}></Route>
    </Routes>
  </Router>
);

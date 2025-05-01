// src/App.jsx
import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";

import LandingPage from "@/pages/LandingPage";
import DesignPage from "@/pages/DesignPage";
import RecommendPage from "@/pages/RecommendPage";
import PlanPage from "@/pages/PlanPage";
import PreviewPage from "@/pages/PreviewPage";

import Navbar from "@/components/layout/Navbar";

function AppRoutes() {
  const location = useLocation();
  const isLanding = location.pathname === "/";

  return (
    <>
      {!isLanding && <Navbar />}
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/design" element={<DesignPage />} />
        <Route path="/recommend" element={<RecommendPage />} />
        <Route path="/plan" element={<PlanPage />} />
        <Route path="/preview" element={<PreviewPage />} />
        <Route
          path="*"
          element={<p className="p-10 text-center">404 Not Found</p>}
        />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <Router>
      <AppRoutes />
    </Router>
  );
}

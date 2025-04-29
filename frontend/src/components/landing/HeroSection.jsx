import React from "react";
import { useNavigate } from "react-router-dom";

export default function HeroSection() {
  const navigate = useNavigate();

  return (
    <div className="relative z-10 flex flex-col items-center justify-center h-screen text-center">
      <h1 className="text-5xl font-extrabold mb-6 tracking-wide drop-shadow-md">
        Design your star journey
      </h1>
      <button
        onClick={() => navigate("/design")}
        className="px-8 py-3 bg-pink-500 hover:bg-pink-600 text-white text-lg font-medium rounded-full shadow-lg transition"
      >
        Design →
      </button>
    </div>
  );
}

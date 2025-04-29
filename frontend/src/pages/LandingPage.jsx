import React from "react";
import Navbar from "../components/layout/Navbar";
import PhoneStack from "../components/landing/PhoneStack";
import HeroSection from "../components/landing/HeroSection";

export default function LandingPage() {
  return (
    <div className="relative min-h-screen bg-black text-white overflow-hidden">
      <Navbar />
      <PhoneStack />
      <HeroSection />
    </div>
  );
}

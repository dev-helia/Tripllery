/**
 * LandingPage.tsx · Tripllery v3 Landing View
 *
 * This is the entry page for the Tripllery experience.
 * It renders the black background hero view with floating phones
 * and a central "Design your star journey" CTA.
 *
 * Composition:
 * ------------
 * - <Navbar />        : transparent top navbar with login button
 * - <PhoneStack />    : blurred background phone card animation (visual delight)
 * - <HeroSection />   : core hero text + animated tagline + bounce CTA button
 *
 * Styling:
 * --------
 * - Background: full black with white text
 * - Absolute-positioned PhoneStack in background
 * - Relative z-index stacking for component layering
 *
 * Used in:
 * --------
 * - Mounted at `/` route (main app entry)
 */

import React from "react";
import Navbar from "../components/layout/Navbar"; // 🧭 顶部导航栏
import PhoneStack from "../components/landing/PhoneStack"; // 📱 背景漂浮手机卡片堆
import HeroSection from "../components/landing/HeroSection"; // 🌟 中央 Hero 标语区

export default function LandingPage() {
  return (
    <div className="relative min-h-screen bg-black text-white overflow-hidden">
      {/* 🔝 透明导航栏 */}
      <Navbar />

      {/* 📱 背景手机卡片层（带模糊+淡出效果） */}
      <PhoneStack />

      {/* 🌟 中央主标题 + tagline + CTA 按钮 */}
      <HeroSection />
    </div>
  );
}

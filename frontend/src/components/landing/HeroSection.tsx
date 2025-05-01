/**
 * HeroSection.tsx · Tripllery v3 Landing Hero
 *
 * This component renders the central hero section of the landing page.
 * Includes animated headline, character-by-character tagline reveal,
 * and bouncing CTA button to start designing a trip.
 *
 * Layout:
 * -------
 * - Title: "Design your star journey" (static)
 * - Tagline: "Your journey. Your vibe. Tripllery it." (animated reveal)
 * - Button: Starts the form flow → /design
 *
 * Animations:
 * -----------
 * ✅ Tagline characters reveal one by one (typing effect)
 * ✅ Blinking cursor "|" after tagline
 * ✅ CTA button bounces to draw attention
 *
 * Props: None
 * State:
 * - visibleCount: number of characters revealed in the tagline
 *
 * Used in: LandingPage.tsx
 */

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import classNames from "classnames";

// 🧾 Tagline content to reveal one character at a time
const taglines = "Your journey. Your vibe. Tripllery it.".split("");

const HeroSection: React.FC = () => {
  const navigate = useNavigate();
  const [visibleCount, setVisibleCount] = useState(0); // 控制显示的字符数

  // 💡 Typing effect: reveal one character at a time
  useEffect(() => {
    const interval = setInterval(() => {
      setVisibleCount((prev) => {
        if (prev >= taglines.length) {
          clearInterval(interval); // 🧼 Stop when done
          return prev;
        }
        return prev + 1;
      });
    }, 60); // 每个字符出现间隔（毫秒）
    return () => clearInterval(interval); // ✅ 清理定时器
  }, []);

  return (
    <div className="relative z-10 flex flex-col items-center justify-center h-screen text-center space-y-6">
      {/* 🌟 Static Title */}
      <h1 className="text-5xl font-extrabold tracking-wide drop-shadow-md">
        Design your star journey
      </h1>

      {/* 🌈 Tagline with typing animation */}
      <p className="text-lg text-pink-200 font-medium h-6">
        {taglines.slice(0, visibleCount).join("")}
        <span className="animate-pulse">|</span> {/* ⌨️ Blinking cursor */}
      </p>

      {/* 💖 CTA Button to Design Page */}
      <button
        onClick={() => navigate("/design")}
        className={classNames(
          "px-8 py-3 mt-2 bg-pink-500 hover:bg-pink-600 text-white text-lg font-medium rounded-full shadow-lg transition pointer-events-auto",
          "animate-bounce delay-1000" // ✨ Bouncy entrance
        )}
      >
        Start Designing →
      </button>
    </div>
  );
};

export default HeroSection;

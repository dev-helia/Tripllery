/**
 * PhoneStack.tsx · Landing Page Background Visuals
 *
 * This component renders a blurred stack of vertical phone-style images
 * behind the main HeroSection, to evoke a sense of memory, travel, and aesthetic layering.
 *
 * Features:
 * ---------
 * ✅ 5 vertically-oriented images in soft rotation
 * ✅ Each image is rotated at a slight angle (-10° to +10°)
 * ✅ Uses Tailwind blur + opacity to act as background layer
 * ✅ Decorative only — aria-hidden + empty alt for accessibility
 *
 * Usage:
 * ------
 * This component is placed as a background layer in LandingPage
 * beneath HeroSection. It creates mood and visual appeal.
 */

import React from "react";

const PhoneStack: React.FC = () => {
  // 🌍 Placeholder image URLs with travel theme
  const placeholderImages: string[] = [
    "https://source.unsplash.com/200x300/?travel,1",
    "https://source.unsplash.com/200x300/?travel,2",
    "https://source.unsplash.com/200x300/?travel,3",
    "https://source.unsplash.com/200x300/?travel,4",
    "https://source.unsplash.com/200x300/?travel,5",
  ];

  // 🔁 Corresponding rotation angles for each card
  const rotationAngles = [-10, -5, 0, 5, 10];

  return (
    <div
      className="
        absolute inset-0 flex justify-center items-center gap-6 
        z-0 opacity-60 blur-sm pointer-events-none
      "
    >
      {placeholderImages.map((url, i) => (
        <div
          key={i}
          className="w-36 h-60 rounded-xl overflow-hidden shadow-lg"
          style={{ transform: `rotate(${rotationAngles[i]}deg)` }}
        >
          <img
            src={url}
            alt="" // Decorative image
            aria-hidden="true" // Accessibility hint: don't read it out
            className="w-full h-full object-cover"
          />
        </div>
      ))}
    </div>
  );
};

export default PhoneStack;

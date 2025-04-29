import React from "react";

export default function PhoneStack() {
  const placeholderImages = [
    "https://source.unsplash.com/200x300/?travel,1",
    "https://source.unsplash.com/200x300/?travel,2",
    "https://source.unsplash.com/200x300/?travel,3",
    "https://source.unsplash.com/200x300/?travel,4",
    "https://source.unsplash.com/200x300/?travel,5",
  ];

  return (
    <div className="absolute inset-0 flex justify-center items-center gap-6 z-0 blur-sm opacity-70">
      {placeholderImages.map((url, i) => (
        <div
          key={i}
          className={`w-36 h-60 rounded-xl overflow-hidden shadow-lg rotate-[${
            -10 + i * 5
          }deg]`}
        >
          <img
            src={url}
            alt={`mock-${i}`}
            className="w-full h-full object-cover"
          />
        </div>
      ))}
    </div>
  );
}

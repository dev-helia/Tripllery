/**
 * POICard.tsx · Tripllery v3 Card Selector UI
 *
 * This component renders a single POI recommendation card,
 * supporting toggle selection, hover animation, and tag display.
 *
 * Main Usage:
 * ------------
 * Appears in the `/selection` route where users choose their favorite POIs.
 * Each card represents one POI, showing image, summary, rating, and tags.
 *
 * Interactivity:
 * --------------
 * ✅ Entire card is clickable (toggle selection)
 * ✅ Top-right ❌ or ➕ icon button toggles card without bubble propagation
 * ✅ Highlighted border when selected (`border-pink-500`)
 *
 * Props:
 * ------
 * - poi: POI object (full structure, from backend)
 * - isSelected: boolean state (selected or not)
 * - onToggle: function to toggle selection
 *
 * Styling:
 * --------
 * TailwindCSS + hover scaling
 * Shadow, rounded corners, responsive image
 * Tag chips rendered in pink tone
 * External links: map + related links
 */

import React from "react";
import { POI } from "@/types/POI"; // ✅ 使用统一前后端字段定义

interface POICardProps {
  poi: POI;
  isSelected: boolean;
  onToggle: () => void;
}

export default function POICard({ poi, isSelected, onToggle }: POICardProps) {
  const {
    name,
    city,
    description,
    rating,
    image_url,
    highlight_tags = [],
    opening_hours = [],
    source,
  } = poi;

  return (
    <div
      className={`relative w-full bg-white rounded-2xl shadow-xl overflow-hidden cursor-pointer transition-all duration-300 hover:scale-[1.02] border-4 ${
        isSelected ? "border-pink-500" : "border-transparent"
      }`}
      onClick={onToggle}
    >
      {/* 📷 Image */}
      <img
        src={image_url || "https://via.placeholder.com/400x300"}
        alt={name}
        className="w-full h-48 object-cover"
      />

      {/* 📑 Card Body */}
      <div className="p-4 space-y-1">
        {/* 🏷️ Name & City */}
        <h2 className="text-lg font-bold text-gray-800">{name}</h2>
        {city && <p className="text-xs text-gray-500">{city}</p>}

        {/* 📝 Description */}
        <p className="text-sm text-gray-600 line-clamp-2">{description}</p>

        {/* ⭐ Rating */}
        <div className="text-xs text-yellow-600">⭐ {rating || "?"}</div>

        {/* 🏷️ Highlight Tags */}
        {highlight_tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-1">
            {highlight_tags.map((tag, i) => (
              <span
                key={i}
                className="bg-pink-100 text-pink-600 text-[10px] font-medium px-2 py-0.5 rounded-full"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}

        {/* 🕐 Opening Hours */}
        {opening_hours.length > 0 && (
          <p className="text-[10px] text-gray-400 mt-1">
            🕐 {opening_hours[0]}
          </p>
        )}

        {/* 🔗 External Links */}
        <div className="mt-2 space-y-1">
          {/* 🔗 Google Maps Link */}
          {source?.google_maps_url && (
            <a
              href={source.google_maps_url}
              target="_blank"
              rel="noopener noreferrer"
              className="block text-xs text-blue-500 hover:underline"
            >
              View on Google Maps ↗
            </a>
          )}

          {/* 🔗 Related Links */}
          {source?.review_links?.length > 0 && (
            <a
              href={source.review_links[0]}
              target="_blank"
              rel="noopener noreferrer"
              className="block text-xs text-indigo-500 hover:underline"
            >
              View Related Link ↗
            </a>
          )}
        </div>
      </div>

      {/* ❤️ Toggle Icon Button */}
      <div
        className="absolute top-2 right-2 bg-white rounded-full p-1 shadow-lg z-10"
        onClick={(e) => {
          e.stopPropagation(); // ❗ prevent bubbling to full card
          onToggle();
        }}
      >
        <span className="text-xl">{isSelected ? "❌" : "➕"}</span>
      </div>
    </div>
  );
}

/**
 * SelectedPanel.tsx · Chosen POIs Display Panel
 *
 * This component renders the left-side panel in the card selection page,
 * displaying all POIs the user has currently selected.
 *
 * Main Usage:
 * ------------
 * Appears in `/selection` route alongside POICard list.
 * Keeps track of selected POIs (from right side) and shows:
 * - Image
 * - Name
 * - Description
 * - City / Rating
 * - ❌ button to remove POI from selectedIds
 *
 * Props:
 * ------
 * - selectedIds: string[] — list of currently selected POI IDs
 * - allCards: POI[] — full POI card list (used to resolve ID → object)
 * - onRemove: (id: string) => void — callback when user clicks remove
 *
 * UX Design:
 * ----------
 * ✅ Empty state with friendly text
 * ✅ Compact summary card (image + text)
 * ✅ Optional Google Maps link
 * ✅ Remove button on top-right corner
 */

import React from "react";
import { POI } from "@/types/POI"; // ✅ 全局统一 POI 类型

interface SelectedPanelProps {
  selectedIds: string[];
  allCards: POI[];
  onRemove: (id: string) => void;
}

export default function SelectedPanel({
  selectedIds,
  allCards,
  onRemove,
}: SelectedPanelProps) {
  // 🧠 Lookup POIs from global list
  const selectedCards = allCards.filter((c) =>
    selectedIds.includes(c.id || "")
  );

  // 💤 Empty state
  if (selectedCards.length === 0) {
    return (
      <div className="text-gray-500 italic">
        You haven’t selected anything yet 💭
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {selectedCards.map((card) => (
        <div
          key={card.id}
          className="relative border border-gray-200 rounded-xl overflow-hidden shadow-sm bg-white"
        >
          {/* 🖼 Image */}
          <img
            src={card.image_url || "https://via.placeholder.com/300x200"}
            alt={card.name}
            className="w-full h-32 object-cover"
          />

          {/* 📄 Text Content */}
          <div className="p-3 space-y-1">
            <h3 className="text-sm font-semibold text-gray-800">{card.name}</h3>
            {card.city && (
              <p className="text-[11px] text-gray-500">{card.city}</p>
            )}
            <p className="text-xs text-gray-600 line-clamp-2">
              {card.description}
            </p>
            <div className="text-[10px] text-yellow-600">
              ⭐ {card.rating || "?"}
            </div>

            {/* 🔗 Google Maps */}
            {card.source?.google_maps_url && (
              <a
                href={card.source.google_maps_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[10px] text-blue-500 hover:underline"
              >
                View on Maps ↗
              </a>
            )}
          </div>

          {/* ❌ Remove Button */}
          <button
            onClick={() => onRemove(card.id!)}
            className="absolute top-2 right-2 bg-white rounded-full shadow-md px-2 text-sm text-red-600 hover:text-red-800"
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
}

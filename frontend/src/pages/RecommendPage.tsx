/**
 * RecommendPage.tsx · Tripllery v3 POI Selection Interface
 *
 * Allows users to pick POIs from the recommendation pool
 * and forwards the selection to /plan generation.
 */

import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { POI } from "@/types/POI";
import POICard from "@/components/cards/POICard";
import SelectedPanel from "@/components/cards/SelectedPanel";
import { getMinRequiredPOIs } from "@/utils/travel";
import { navigateWithPayload } from "@/utils/navigateWithPayload";

export default function RecommendPage(): JSX.Element {
  const location = useLocation();
  const navigate = useNavigate();

  /** ---------------- incoming state ---------------- */
  const formData = location.state?.formData ?? {};
  const initial = (location.state?.cards as POI[]) ?? [];

  /** ---------------- business calc ----------------- */
  const minRequired =
    location.state?.min_required ??
    getMinRequiredPOIs(
      formData.start_datetime,
      formData.end_datetime,
      formData.intensity ?? "normal"
    );

  /** ---------------- local state ------------------- */
  const [cards, setCards] = useState<POI[]>(initial);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [loadingMore, setLoadingMore] = useState(false);

  /** 选择 / 反选一张卡 */
  const toggleSelect = (id: string) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  /** 🚀 提交 → /plan */
  const handleSubmit = () => {
    navigateWithPayload(navigate, "/plan", {
      formData,
      accepted_pois: selectedIds, // ✅ ids for backend
      all_pois: cards, // full pool
      min_required: minRequired, // optional meta
    });
  };

  /** 继续向后端拉更多卡片 */
  const loadMoreCards = async () => {
    setLoadingMore(true);
    try {
      const res = await fetch(`/recommend/more?start=${cards.length}&size=6`);
      const data = await res.json();
      setCards((prev) => [...prev, ...(data.cards ?? [])]);
    } catch (err) {
      console.error("❌ Failed to load more POIs:", err);
    } finally {
      setLoadingMore(false);
    }
  };

  /* ==============  UI  ============== */
  return (
    <div className="min-h-screen bg-white px-6 py-8 space-y-6">
      {/* header */}
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Select Your POIs 🗺️</h2>
        <button
          onClick={handleSubmit}
          disabled={selectedIds.length < minRequired}
          className={`px-4 py-2 rounded text-white font-bold transition
            ${
              selectedIds.length < minRequired
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-700"
            }`}
        >
          I’m Done →
        </button>
      </div>

      {/* counter */}
      <p className="text-sm text-gray-600">
        Selected {selectedIds.length} / {minRequired} required&nbsp;
        <span className="text-gray-400 italic">
          (based on trip days × style intensity)
        </span>
      </p>

      {/* grid layout */}
      <div className="grid grid-cols-2 gap-6">
        {/* left: selected */}
        <div className="space-y-4">
          <h3 className="font-medium">❤️ Selected</h3>
          <SelectedPanel
            selectedIds={selectedIds}
            allCards={cards}
            onRemove={(id) =>
              setSelectedIds(selectedIds.filter((x) => x !== id))
            }
          />
        </div>

        {/* right: pool */}
        <div>
          <div className="grid grid-cols-2 gap-4">
            {cards.map((card) => (
              <POICard
                key={card.id}
                poi={card}
                isSelected={selectedIds.includes(card.id)}
                onToggle={() => toggleSelect(card.id)}
              />
            ))}
          </div>

          {/* load-more */}
          <div className="flex justify-center mt-6">
            <button
              onClick={loadMoreCards}
              disabled={loadingMore}
              className="text-sm text-pink-600 hover:underline"
            >
              {loadingMore ? "Loading…" : "More Cards →"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

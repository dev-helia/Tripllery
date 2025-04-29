import React, { useState } from "react";
import POICard from "./POICard";
import { useLocation, useNavigate } from "react-router-dom";

interface POI {
  id: string;
  name: string;
  description: string;
  rating?: number;
  image_url?: string;
  highlight_tags?: string[];
}

interface SwipeDeckProps {
  cards: POI[];
  currentIndex: number;
  setCurrentIndex: (index: number) => void;
}

export default function SwipeDeck({
  cards,
  currentIndex,
  setCurrentIndex,
}: SwipeDeckProps) {
  const [likedCards, setLikedCards] = useState<POI[]>([]);
  const navigate = useNavigate();
  const location = useLocation();

  const formData = location.state?.formData;
  const start = new Date(formData.start_datetime);
  const end = new Date(formData.end_datetime);
  const intensity = formData.intensity || "normal";

  // Calculate trip duration in days
  const dayCount =
    Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)) + 1;

  // Define minimum POI requirements based on trip intensity
  const minRequired =
    intensity === "chill"
      ? dayCount
      : intensity === "intense"
      ? dayCount * 3
      : dayCount * 2;

  const handleLike = (card: POI) => {
    if (!likedCards.find((c) => c.id === card.id)) {
      setLikedCards([...likedCards, card]);
    }
    setCurrentIndex(currentIndex + 1);
  };

  const handleSkip = () => {
    setCurrentIndex(currentIndex + 1);
  };

  const handleSubmitPlan = async () => {
    if (likedCards.length < minRequired) {
      alert(
        `You need to select at least ${minRequired} POIs to generate a trip plan.`
      );
      return;
    }

    try {
      const res = await fetch("/plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          form_data: formData,
          selected_pois: likedCards,
        }),
      });

      if (!res.ok) throw new Error("Plan generation failed");

      const result = await res.json();
      navigate("/plan", {
        state: {
          plan: result.plan,
          formData,
          selectedPOIs: likedCards,
        },
      });
    } catch (err) {
      alert("Failed to generate plan. Please try again later.");
    }
  };

  return (
    <div className="relative w-full max-w-md h-[450px] mx-auto">
      {cards.map((card, index) => (
        <div
          key={card.id}
          className={`absolute top-0 left-0 w-full transition-all duration-300 ${
            index === currentIndex ? "opacity-100 z-10" : "opacity-0 z-0"
          }`}
        >
          <POICard poi={card} />
          <div className="flex justify-around mt-4">
            <button
              onClick={handleSkip}
              className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
            >
              Skip
            </button>
            <button
              onClick={() => handleLike(card)}
              className="px-4 py-2 bg-pink-500 text-white rounded hover:bg-pink-600"
            >
              ❤️ Like
            </button>
          </div>
        </div>
      ))}

      {/* Submit button after all cards are swiped */}
      {currentIndex >= cards.length && (
        <div className="mt-6 text-center">
          <p className="mb-3 text-sm text-gray-500">
            You selected {likedCards.length} cards. Minimum required:{" "}
            {minRequired}
          </p>
          <button
            onClick={handleSubmitPlan}
            className="w-full py-2 bg-pink-500 text-white rounded hover:bg-pink-600"
          >
            ✅ Submit and Generate Itinerary
          </button>
        </div>
      )}
    </div>
  );
}

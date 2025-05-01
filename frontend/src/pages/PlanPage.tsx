/**
 * PlanPage.tsx · Tripllery v3
 *
 * This page handles:
 * 1️⃣ Submitting selected POIs to the `/plan` backend
 * 2️⃣ Receiving the per-day grouped plan + original options
 * 3️⃣ Displaying plan summary and allowing transition to preview
 *
 * Comes after: /recommend
 * Goes to: /preview
 */

import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { POI } from "@/types/POI";
import { navigateWithPayload } from "@/utils/navigateWithPayload";

// -----------------------------
// 🧭 Main Component
// -----------------------------
export default function PlanPage(): JSX.Element {
  const location = useLocation();
  const navigate = useNavigate();

  const {
    accepted_pois = [],
    all_pois = [],
    formData = {},
  } = location.state || {};

  const [plan, setPlan] = useState<Record<string, POI[]> | null>(null);
  const [options, setOptions] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);

  // 📡 Request the detailed day-by-day plan from backend
  useEffect(() => {
    const fetchPlan = async () => {
      try {
        const res = await fetch("/plan", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            accepted_pois,
            all_pois,
            ...formData,
          }),
        });

        const result = await res.json();
        setPlan(result.plan || {});
        setOptions(result.options || {});
      } catch (err) {
        console.error("❌ Failed to fetch plan:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchPlan();
  }, []);

  // 🌀 Loading state
  if (loading) {
    return (
      <p className="text-center py-10 text-gray-500">Generating plan...</p>
    );
  }

  // ❌ No plan data fallback
  if (!plan || Object.keys(plan).length === 0) {
    return (
      <p className="text-center py-10 text-red-500">No plan data found.</p>
    );
  }

  // ✨ Go to /preview (using helper)
  const handlePreview = () => {
    navigateWithPayload(navigate, "/preview", {
      formData,
      all_pois, // if needed by PreviewPage
      cards: [], // optional (empty for now)
    });

    // 🧭 Also pass detailed plan and options
    navigate("/preview", {
      state: {
        plan,
        options,
      },
    });
  };

  return (
    <div className="max-w-4xl mx-auto py-12 px-6 text-gray-800">
      <h1 className="text-2xl font-bold mb-8 text-center">Your Trip Plan</h1>

      {/* 🔗 Preview Button */}
      <div className="text-center mb-6">
        <button
          onClick={handlePreview}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded font-semibold transition"
        >
          ✨ Preview Your Full Trip →
        </button>
      </div>

      {/* 🗓️ Display grouped POIs per day */}
      <div className="space-y-8">
        {Object.entries(plan).map(([day, pois]) => (
          <div key={day} className="bg-gray-50 border rounded shadow p-6">
            <h2 className="font-semibold text-lg mb-4 text-pink-600">{day}</h2>

            <ul className="space-y-4">
              {pois.map((poi, idx) => (
                <li
                  key={poi.id || idx}
                  className="border rounded p-4 bg-white shadow-sm"
                >
                  {/* 📷 Image Preview */}
                  {poi.image_url && (
                    <img
                      src={poi.image_url}
                      alt={poi.name}
                      className="w-full h-32 object-cover rounded mb-2"
                    />
                  )}

                  {/* 📋 POI Info */}
                  <div className="font-semibold text-lg mb-1">{poi.name}</div>

                  {poi.highlight_tags?.length > 0 && (
                    <div className="text-sm text-gray-500 mb-1">
                      Tags: {poi.highlight_tags.join(", ")}
                    </div>
                  )}

                  {poi.rating && (
                    <div className="text-sm text-yellow-500">
                      ⭐ {poi.rating}
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

/**
 * PlanPage.tsx · Tripllery v3
 *
 * - POST /plan 生成每日分组
 * - 展示结果并跳转到 /preview
 */

import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { POI } from "@/types/POI";

export default function PlanPage(): JSX.Element {
  const location = useLocation();
  const navigate = useNavigate();

  /* ------------------------------------------------------------------ */
  /* 🔗 取上一步 /recommend 传来的数据                                   */
  /* ------------------------------------------------------------------ */
  const {
    accepted_pois = [],
    all_pois = [],
    formData = {},
  } = location.state || {};

  const [plan, setPlan] = useState<Record<string, POI[]> | null>(null);
  const [options, setOptions] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);

  /* ------------------------------------------------------------------ */
  /* 📡 请求 /plan                                                      */
  /* ------------------------------------------------------------------ */
  useEffect(() => {
    (async () => {
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

        if (!res.ok) throw new Error("Plan API error");
        const result = await res.json();
        setPlan(result.plan || {});
        setOptions(result.options || {});
      } catch (err) {
        console.error("❌ Failed to fetch plan:", err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  /* ------------------------------------------------------------------ */
  /* ⏳ Loading / Error                                                  */
  /* ------------------------------------------------------------------ */
  if (loading)
    return <p className="text-center py-10 text-gray-500">Generating plan…</p>;

  if (!plan || Object.keys(plan).length === 0)
    return (
      <p className="text-center py-10 text-red-500">No plan data found.</p>
    );

  /* ------------------------------------------------------------------ */
  /* ✨ 跳转到 /preview —— 这一次把 formData / all_pois 一并带过去        */
  /* ------------------------------------------------------------------ */
  const handlePreview = () => {
    navigate("/preview", {
      state: {
        plan,
        options,
        formData,
        all_pois,
      },
    });
  };

  /* ------------------------------------------------------------------ */
  /* 🎨 Render                                                          */
  /* ------------------------------------------------------------------ */
  return (
    <div className="max-w-4xl mx-auto py-12 px-6 text-gray-800">
      <h1 className="text-2xl font-bold mb-8 text-center">Your Trip Plan</h1>

      <div className="text-center mb-6">
        <button
          onClick={handlePreview}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded font-semibold transition"
        >
          ✨ Preview Your Full Trip →
        </button>
      </div>

      {Object.entries(plan).map(([day, pois]) => (
        <div key={day} className="bg-gray-50 border rounded shadow p-6 mb-8">
          <h2 className="font-semibold text-lg mb-4 text-pink-600">{day}</h2>

          <ul className="space-y-4">
            {pois.map((poi, idx) => (
              <li
                key={poi.id || idx}
                className="border rounded p-4 bg-white shadow-sm"
              >
                {poi.image_url && (
                  <img
                    src={poi.image_url}
                    alt={poi.name}
                    className="w-full h-32 object-cover rounded mb-2"
                  />
                )}

                <div className="font-semibold text-lg mb-1">{poi.name}</div>

                {poi.highlight_tags?.length > 0 && (
                  <div className="text-sm text-gray-500 mb-1">
                    Tags: {poi.highlight_tags.join(", ")}
                  </div>
                )}

                {poi.rating && (
                  <div className="text-sm text-yellow-500">⭐ {poi.rating}</div>
                )}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

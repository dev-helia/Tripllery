/**
 * PreviewPage.tsx · Tripllery v3
 *
 * 4-Quadrant preview (Map · TextTimeline · TimeAxis · Calendar)
 * + “Edit this trip” button
 * + POI-detail modal opened via onViewDetail(id)
 */

import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import dayjs from "dayjs";

import MapPanel from "@/components/preview/MapPanel";
import TextTimeline from "@/components/preview/TextTimeline";
import TimeAxis from "@/components/preview/TimeAxis";
import CalendarPanel from "@/components/preview/CalendarPanel";

import Modal from "@/components/ui/Modal";
import POICard from "@/components/cards/POICard";

import { useTimelineSelection } from "@/hooks/useTimelineSelection";
import { TimelineBlock } from "@/types/TimelineBlock";
import { POI } from "@/types/POI";

type TimelineData = Record<string, TimelineBlock[]>;

export default function PreviewPage(): JSX.Element {
  const location = useLocation();
  const navigate = useNavigate();

  /* ------------------------------------------------------------------ */
  /* 📦  Data passed from PlanPage                                       */
  /* ------------------------------------------------------------------ */
  const {
    plan: roughPlan = {},
    options = {},
    formData = {},
    all_pois: allPOIs = [],
  } = location.state || {};

  const fallbackStart = Object.keys(roughPlan)[0] || "";
  const fallbackEnd = Object.keys(roughPlan).slice(-1)[0] || "";

  const startDate = options?.start_datetime || fallbackStart;
  const endDate = options?.end_datetime || fallbackEnd;

  /* ------------------------------------------------------------------ */
  /* 🛠️  Local state                                                    */
  /* ------------------------------------------------------------------ */
  const [selectedDay, setSelectedDay] = useState<string>(fallbackStart);
  const [timelineByDate, setTimelineByDate] = useState<TimelineData>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /* 👉 Modal state for POI detail */
  const [showModal, setShowModal] = useState(false);
  const [modalContent, setModalContent] = useState<POI | null>(null);

  /* Shared highlight-ID hook (map / timeline / axis) */
  const { activeId, setActiveId } = useTimelineSelection();

  /* ------------------------------------------------------------------ */
  /* 🔄  Fetch full timeline from backend                                */
  /* ------------------------------------------------------------------ */
  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const res = await fetch("/preview", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ plan: roughPlan, options }),
        });
        if (!res.ok) throw new Error("Preview API error");

        const raw: TimelineData = await res.json();
        const fixed: TimelineData = {};
        for (const k in raw) fixed[dayjs(k).format("YYYY-MM-DD")] = raw[k];

        setTimelineByDate(fixed);
        setSelectedDay(Object.keys(fixed)[0] || "");
      } catch (err) {
        console.error("❌ Preview fetch error:", err);
        setError("Failed to generate trip preview.");
      } finally {
        setLoading(false);
      }
    })();
  }, [roughPlan, options]);

  /* ------------------------------------------------------------------ */
  /* ↩️  Edit-trip button handler                                        */
  /* ------------------------------------------------------------------ */
  const handleEditTrip = () => {
    navigate("/design", {
      state: {
        formData,
        all_pois: allPOIs,
        // selectedIds can also be passed back if you store them
      },
    });
  };

  /* ------------------------------------------------------------------ */
  /* 🔍  View-detail handler → opens modal                               */
  /* ------------------------------------------------------------------ */
  const handleViewDetail = (id: string) => {
    const poi = allPOIs.find((p) => p.id === id);
    if (poi) {
      setModalContent(poi);
      setShowModal(true);
    }
  };

  /* ------------------------------------------------------------------ */
  /* ⏳ Loading / Error                                                  */
  /* ------------------------------------------------------------------ */
  if (loading)
    return <p className="text-center py-10 text-gray-500">Loading preview…</p>;
  if (error) return <p className="text-center py-10 text-red-500">{error}</p>;

  const currentBlocks = timelineByDate[selectedDay] || [];

  /* ------------------------------------------------------------------ */
  /* 🎨 Render                                                           */
  /* ------------------------------------------------------------------ */
  return (
    <>
      {/* ────────── Top-bar with “Edit” link ────────── */}
      <div className="flex justify-end px-6">
        <button
          onClick={handleEditTrip}
          className="text-sm text-indigo-600 hover:underline"
        >
          ← Edit this trip
        </button>
      </div>

      {/* ────────── 4-Quadrant Layout ────────── */}
      <div className="flex gap-6 p-6 max-w-7xl mx-auto text-gray-800 h-[90vh]">
        {/* ⬅️ Map + TextTimeline */}
        <div className="flex flex-col w-[60%] gap-4 overflow-hidden">
          <div className="h-[300px] border rounded bg-white shadow p-4">
            <MapPanel
              mapBlocks={currentBlocks}
              activeId={activeId}
              onSelectPOI={setActiveId}
            />
          </div>

          <div className="flex-1 border rounded bg-white shadow p-4 overflow-y-auto">
            {currentBlocks.length === 0 ? (
              <p className="text-center text-sm text-gray-400">
                No itinerary for this day.
              </p>
            ) : (
              <TextTimeline
                key={selectedDay}
                data={currentBlocks}
                activeId={activeId}
                onHover={setActiveId}
                onViewDetail={handleViewDetail} // 🆕 detail hook
              />
            )}
          </div>
        </div>

        {/* ➡️ Calendar + TimeAxis */}
        <div className="flex flex-col w-[40%] gap-4 overflow-hidden">
          <div className="border rounded bg-white shadow p-4 h-fit">
            <CalendarPanel
              startDate={startDate}
              endDate={endDate}
              selectedDate={selectedDay}
              onSelect={(d) => setSelectedDay(dayjs(d).format("YYYY-MM-DD"))}
            />
          </div>

          <div className="flex-1 border rounded bg-white shadow p-4 overflow-y-auto">
            <TimeAxis
              data={currentBlocks}
              activeId={activeId}
              onHover={setActiveId}
            />
          </div>
        </div>
      </div>

      {/* ────────── POI Detail Modal ────────── */}
      {showModal && modalContent && (
        <Modal onClose={() => setShowModal(false)}>
          <POICard poi={modalContent} isSelected={false} onToggle={() => {}} />
        </Modal>
      )}
    </>
  );
}

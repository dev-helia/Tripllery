/**
 * PreviewPage.tsx · Tripllery v3 Timeline Preview View
 *
 * This page renders a 4-quadrant layout to preview a generated travel plan:
 * 🗺️ MapPanel: map view with polylines + POI markers
 * 📋 TextTimeline: text timeline list per day
 * ⏳ TimeAxis: vertical visual timeline by hour
 * 📆 CalendarPanel: calendar date selector with Day X of Y highlight
 *
 * Data:
 * -----
 * Receives:
 * - plan: day-wise POI blocks (from PlanPage)
 * - options: form data used to generate timeline
 *
 * On first render, immediately calls POST /preview to retrieve detailed schedule.
 */

import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

import TextTimeline from "../components/preview/TextTimeline";
import CalendarPanel from "../components/preview/CalendarPanel";
import MapPanel from "../components/preview/MapPanel";
import TimeAxis from "../components/preview/TimeAxis";

import { useTimelineSelection } from "../hooks/useTimelineSelection";
import dayjs from "dayjs";

import { TimelineBlock } from "@/types/TimelineBlock"; // ✅ use global unified type

type TimelineData = Record<string, TimelineBlock[]>;

export default function PreviewPage(): JSX.Element {
  const location = useLocation();
  const state = location.state || {};

  const roughPlan: TimelineData = state.plan || {};
  const options = state.options || {};

  const fallbackStart = Object.keys(roughPlan)[0] || "";
  const fallbackEnd = Object.keys(roughPlan).slice(-1)[0] || "";

  const startDate = options?.start_datetime || fallbackStart;
  const endDate = options?.end_datetime || fallbackEnd;

  const [selectedDay, setSelectedDay] = useState<string>(fallbackStart);
  const [timelineByDate, setTimelineByDate] = useState<TimelineData>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const { activeId, setActiveId } = useTimelineSelection();

  /**
   * 🔄 Fetches full timeline details from backend
   */
  useEffect(() => {
    async function fetchPreview() {
      try {
        setLoading(true);
        const res = await fetch("/preview", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            plan: roughPlan,
            options: options,
          }),
        });

        if (!res.ok) throw new Error("Failed to fetch preview timeline.");

        const rawData: TimelineData = await res.json();

        // 🔧 Normalize keys to YYYY-MM-DD format
        const fixed: TimelineData = {};
        for (const key in rawData) {
          const formatted = dayjs(key).format("YYYY-MM-DD");
          fixed[formatted] = rawData[key];
        }

        setTimelineByDate(fixed);
        setSelectedDay(Object.keys(fixed)[0] || "");
        setError(null);
      } catch (err) {
        console.error("❌ Preview fetch error:", err);
        setError("Failed to generate trip preview.");
      } finally {
        setLoading(false);
      }
    }

    if (roughPlan && Object.keys(roughPlan).length > 0) {
      fetchPreview();
    }
  }, [roughPlan, options]);

  const handleSelectDay = (day: string) => {
    const formatted = dayjs(day).format("YYYY-MM-DD");
    setSelectedDay(formatted);
  };

  const currentDayBlocks = timelineByDate[selectedDay] || [];

  if (loading) {
    return (
      <p className="text-center py-10 text-gray-500">Loading preview...</p>
    );
  }

  if (error) {
    return <p className="text-center py-10 text-red-500">{error}</p>;
  }

  return (
    <div className="flex gap-6 p-6 max-w-7xl mx-auto text-gray-800 h-[90vh]">
      {/* ⬅️ Left: Map + Text timeline */}
      <div className="flex flex-col w-[60%] gap-4 overflow-hidden">
        <div className="h-[300px] border rounded bg-white shadow p-4">
          <MapPanel
            mapBlocks={currentDayBlocks}
            activeId={activeId}
            onSelectPOI={setActiveId}
          />
        </div>

        <div className="flex-1 border rounded bg-white shadow p-4 overflow-y-auto">
          {currentDayBlocks.length === 0 ? (
            <p className="text-center text-sm text-gray-400">
              No itinerary for this day.
            </p>
          ) : (
            <TextTimeline
              data={currentDayBlocks}
              activeId={activeId}
              onHover={setActiveId}
              key={selectedDay}
            />
          )}
        </div>
      </div>

      {/* ➡️ Right: Calendar + Time Axis */}
      <div className="flex flex-col w-[40%] gap-4 overflow-hidden">
        <div className="border rounded bg-white shadow p-4 h-fit">
          <CalendarPanel
            startDate={startDate}
            endDate={endDate}
            selectedDate={selectedDay}
            onSelect={handleSelectDay}
          />
        </div>

        <div className="flex-1 border rounded bg-white shadow p-4 overflow-y-auto">
          <TimeAxis
            data={currentDayBlocks}
            activeId={activeId}
            onHover={setActiveId}
          />
        </div>
      </div>
    </div>
  );
}

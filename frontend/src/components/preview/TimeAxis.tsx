/**
 * TimeAxis.tsx · Tripllery v3 Preview Timeline (Vertical Axis View)
 *
 * This component renders a vertical 24-hour axis, placing activity blocks
 * (Sightseeing, Meal, Transportation, etc.) based on their start/end time.
 *
 * Props:
 * -------
 * - data: array of schedule blocks (with day, start_time, end_time, type, etc.)
 * - activeId: optional currently focused block ID (for syncing with map/timeline)
 * - onHover: callback when a block is hovered (for external sync)
 *
 * Features:
 * ---------
 * ✅ Fixed vertical scale: 1440px → 1px = 1 minute
 * ✅ Activity blocks positioned accurately by time
 * ✅ Block coloring by type (Meal, Sightseeing, etc.)
 * ✅ Free-time gaps ≥ 30min shown as ⏳ placeholders
 * ✅ Hover feedback with ring + tooltip
 * ✅ Error fallback for invalid/missing time strings
 *
 * Data source: `POST /preview` full_schedule[day] ➔ preview blocks
 */

import React from "react";
import classNames from "classnames";
import { TimelineBlock } from "@/types/TimelineBlock"; // ✅ use global type

// -----------------------
// 🔧 Props
// -----------------------

interface Props {
  data: TimelineBlock[];
  activeId?: string;
  onHover?: (id?: string) => void;
}

// -----------------------
// ⏱️ Helper: Convert "HH:MM" ➜ total minutes
// -----------------------
function timeToMinutes(time: string | undefined): number {
  if (!time || typeof time !== "string" || !time.includes(":")) {
    console.warn("⚠️ Invalid time format in TimeAxis:", time);
    return 0;
  }
  const [h, m] = time.split(":").map(Number);
  return h * 60 + m;
}

// -----------------------
// 🧭 Main Component
// -----------------------

export default function TimeAxis({ data, activeId, onHover }: Props) {
  // 🧹 过滤掉缺时间的 block
  const validBlocks = data.filter(
    (block) => block?.start_time && block?.end_time
  );

  const sorted = [...validBlocks].sort(
    (a, b) => timeToMinutes(a.start_time) - timeToMinutes(b.start_time)
  );

  const hours = Array.from(
    { length: 24 },
    (_, i) => `${i.toString().padStart(2, "0")}:00`
  );

  const allBlocks: JSX.Element[] = [];

  for (let i = 0; i < sorted.length; i++) {
    const current = sorted[i];
    const next = sorted[i + 1];

    const start = timeToMinutes(current.start_time);
    const end = timeToMinutes(current.end_time);
    const top = (start / 1440) * 100;
    const height = ((end - start) / 1440) * 100;

    // 🎨 样式映射
    const color =
      current.type === "Meal"
        ? "bg-green-100 border-green-400"
        : current.type === "Sightseeing"
        ? "bg-blue-100 border-blue-400"
        : current.type === "Transportation"
        ? "bg-yellow-100 border-yellow-400"
        : "bg-gray-100 border-gray-400";

    // 📦 活动块渲染
    allBlocks.push(
      <div
        key={`block-${i}`}
        title={`${current.start_time} - ${current.end_time}`}
        className={classNames(
          "absolute left-0 right-2 rounded-md border-l-4 px-3 py-1 text-sm shadow-sm transition cursor-pointer overflow-hidden",
          color,
          {
            "ring-2 ring-indigo-500": current.id === activeId,
          }
        )}
        style={{
          top: `${top}%`,
          height: `${height}%`,
        }}
        onMouseEnter={() => onHover?.(current.id)}
        onMouseLeave={() => onHover?.()}
      >
        <div className="font-medium">{current.activity}</div>
        <div className="text-xs text-gray-500">
          {current.start_time} - {current.end_time}
        </div>
      </div>
    );

    // ✨ 插入空隙提示块（≥30min 的间隔）
    if (next) {
      const gap =
        timeToMinutes(next.start_time) - timeToMinutes(current.end_time);
      if (gap >= 30) {
        const gapTop = (timeToMinutes(current.end_time) / 1440) * 100;
        const gapHeight = (gap / 1440) * 100;

        allBlocks.push(
          <div
            key={`gap-${i}`}
            className="absolute left-0 right-2 px-2 text-[10px] italic text-gray-400 flex items-center justify-center"
            style={{
              top: `${gapTop}%`,
              height: `${gapHeight}%`,
            }}
          >
            ⏳ Free time: {Math.floor(gap / 60)}h
            {gap % 60 ? ` ${gap % 60}m` : ""}
          </div>
        );
      }
    }
  }

  return (
    <div className="relative h-[1440px] border-l border-gray-200 overflow-hidden bg-white">
      {/* 🕓 左侧时间刻度 */}
      <div className="absolute left-0 top-0 w-14">
        {hours.map((h) => (
          <div
            key={h}
            className="h-[60px] text-[11px] text-gray-400 text-right pr-2 border-t border-gray-100"
          >
            {h}
          </div>
        ))}
      </div>

      {/* 🧱 活动区 */}
      <div className="ml-16 relative h-full">
        {allBlocks.length > 0 ? (
          allBlocks
        ) : (
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 text-sm text-gray-400">
            ⚠️ No valid schedule data to render.
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * TextTimeline.tsx · Tripllery v3 Preview Timeline (Text List)
 *
 * Displays a scrollable list of schedule blocks for a selected day,
 * usually synced with the calendar, time axis, and map.
 *
 * Props:
 * -------
 * - data: TimelineBlock[] (from full_schedule[date])
 * - activeId: the ID of the currently highlighted block
 * - onHover: triggers highlight sync on hover
 * - onClick: triggers day-switch or map focus on click
 * - onViewDetail: 🔍 optional detail viewer, used to open modal
 *
 * Features:
 * ---------
 * ✅ Sync highlight with map and timeline
 * ✅ Mini image preview
 * ✅ Tag display
 * ✅ "View Details" button to trigger POI modal
 */

import React from "react";
import classNames from "classnames";
import { TimelineBlock } from "@/types/TimelineBlock"; // ✅ Use global shared type

interface Props {
  data: TimelineBlock[];
  activeId?: string;
  onHover?: (id?: string) => void;
  onClick?: (id?: string) => void;
  onViewDetail?: (id: string) => void;
}

export default function TextTimeline({
  data,
  activeId,
  onHover,
  onClick,
  onViewDetail,
}: Props): JSX.Element {
  // 🧼 Empty fallback UI
  if (!data || data.length === 0) {
    return (
      <div className="text-gray-400 text-sm italic text-center py-10">
        📭 No activities scheduled for this day. <br />
        But hey — why not play a random song and chill? 🎧
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 overflow-y-auto max-h-[600px] pr-1">
      {data.map((block) => {
        const isActive = block.id === activeId;
        const blockKey = block.id || `${block.activity}-${block.start_time}`;

        return (
          <div
            key={blockKey}
            onMouseEnter={() => onHover?.(block.id)}
            onMouseLeave={() => onHover?.()}
            onClick={() => onClick?.(block.id)}
            className={classNames(
              "flex gap-3 items-start p-3 rounded-md shadow-sm border transition cursor-pointer bg-white",
              {
                "ring-2 ring-indigo-400 bg-indigo-50": isActive,
                "hover:bg-gray-50": !isActive,
              }
            )}
          >
            {/* 📷 Image */}
            {block.image_url ? (
              <img
                src={block.image_url}
                alt={block.activity}
                className="w-16 h-16 object-cover rounded-md flex-shrink-0"
              />
            ) : (
              <div className="w-16 h-16 bg-gray-200 rounded-md flex items-center justify-center text-xs text-gray-500">
                🗺️
              </div>
            )}

            {/* 📋 Block content */}
            <div className="flex flex-col flex-1">
              <div className="text-sm font-semibold text-gray-800">
                {block.activity}
              </div>
              <div className="text-xs text-gray-500 mb-1">
                🕒 {block.start_time} - {block.end_time}
              </div>

              {/* 🏷️ Tags */}
              <div className="flex flex-wrap gap-1 mb-1">
                {(block.highlight_tags || []).map((tag, i) => (
                  <span
                    key={`${tag}-${i}`}
                    className="text-[10px] bg-pink-100 text-pink-600 px-2 py-[2px] rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>

              {/* 🔍 View Detail */}
              {block.id && (
                <button
                  className="text-[10px] text-indigo-600 hover:underline self-start"
                  onClick={(e) => {
                    e.stopPropagation(); // Prevent bubbling to parent
                    onViewDetail?.(block.id);
                  }}
                >
                  View Details ↗
                </button>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

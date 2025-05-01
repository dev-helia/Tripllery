import { useState, useCallback } from "react";

/**
 * useTimelineSelection.ts · Tripllery v3 Preview Sync Hook
 *
 * Global sync hook for managing currently active timeline block across views.
 * Used to coordinate shared highlight state across:
 * - 🧭 TextTimeline (textual schedule list)
 * - 🗺️ MapPanel (POI markers and polylines)
 * - ⏱️ TimeAxis (vertical timeline of the day)
 *
 * Features:
 * ---------
 * ✅ Share active block ID across all preview subcomponents
 * ✅ Hover or click triggers highlight
 * ✅ Clean, isolated hook for preview sync logic
 *
 * Returns:
 * --------
 * - activeId: string | null — the currently focused block ID
 * - setActiveId(id: string | null): void — setter for activating or clearing focus
 */
export function useTimelineSelection() {
  const [activeId, setActiveId] = useState<string | null>(null);

  // 🔁 Hover 或点击某个块时调用
  const setActive = useCallback((id: string | null) => {
    setActiveId(id);
  }, []);

  return {
    activeId, // 当前高亮的 ID
    setActiveId: setActive, // 用于传入子组件的回调
  };
}

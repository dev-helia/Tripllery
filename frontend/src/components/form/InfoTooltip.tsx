import React from "react";

interface InfoTooltipProps {
  message: string;
  position?: "top" | "right"; // ✨可选方向（默认向上）
}

/**
 * 🧠 InfoTooltip.tsx
 *
 * A small (❓) icon with hover tooltip.
 * Can show info above or beside the icon.
 *
 * Props:
 * ------
 * - message: Tooltip text
 * - position: "top" (default) | "right"
 */
export default function InfoTooltip({
  message,
  position = "top",
}: InfoTooltipProps) {
  const baseTooltip =
    "absolute z-50 bg-gray-800 text-white text-sm rounded px-2 py-1 whitespace-normal w-48";
  const posClass =
    position === "top"
      ? "bottom-full mb-2 left-1/2 transform -translate-x-1/2"
      : "left-full ml-2 top-1/2 transform -translate-y-1/2";

  return (
    <div className="group relative flex items-center ml-2 cursor-pointer">
      {/* ❓ Icon */}
      <div className="w-5 h-5 rounded-full bg-gray-400 text-white text-[10px] font-bold flex items-center justify-center hover:bg-gray-600 transition-all">
        ?
      </div>

      {/* 📌 Tooltip */}
      <div className={`${baseTooltip} ${posClass} hidden group-hover:block`}>
        {message}
      </div>
    </div>
  );
}

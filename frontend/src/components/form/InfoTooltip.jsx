import React from "react";

export default function InfoTooltip({ message }) {
  return (
    <div className="group relative flex items-center cursor-pointer ml-2">
      <div className="w-4 h-4 rounded-full bg-gray-400 text-white text-xs flex items-center justify-center">
        ?
      </div>
      <div className="absolute bottom-full mb-2 hidden group-hover:block w-40 bg-gray-800 text-white text-sm rounded px-2 py-1 z-50">
        {message}
      </div>
    </div>
  );
}

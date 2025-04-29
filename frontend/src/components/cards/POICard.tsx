import React from "react";

interface POI {
  id?: string;
  name: string;
  description: string;
  rating?: number;
  image_url?: string;
  highlight_tags?: string[];
}

interface POICardProps {
  poi: POI;
}

export default function POICard({ poi }: POICardProps) {
  const { name, description, rating, image_url, highlight_tags = [] } = poi;

  return (
    <div className="w-full max-w-md bg-white rounded-2xl shadow-xl overflow-hidden transform transition-all duration-300 hover:scale-[1.015]">
      <img
        src={image_url || "https://via.placeholder.com/400x300"}
        alt={name}
        className="w-full h-64 object-cover"
      />
      <div className="p-6 space-y-2">
        <h2 className="text-2xl font-bold text-gray-800">{name}</h2>
        <p className="text-sm text-gray-500 line-clamp-3">{description}</p>
        <div className="flex items-center text-sm text-yellow-600 mt-1">
          ⭐ {rating || "?"}
        </div>
        <div className="flex flex-wrap gap-2 mt-3">
          {highlight_tags.map((tag, i) => (
            <span
              key={i}
              className="bg-pink-100 text-pink-600 text-xs font-medium px-3 py-1 rounded-full"
            >
              #{tag}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

/**
 * MapPanel.tsx · Tripllery v3 Preview Map Viewer
 *
 * This component renders the full-trip map view using Google Maps,
 * including POI markers, transportation polylines, and InfoWindows.
 *
 * Props:
 * -------
 * - mapBlocks: array of POI blocks (with lat/lng) and Route blocks (with polyline)
 * - activeId: currently focused POI id (for highlighting)
 * - onSelectPOI: callback when user clicks on a marker
 *
 * Features:
 * ---------
 * ✅ Renders POI markers from daily schedule
 * ✅ Displays transportation paths using polylines
 * ✅ Supports InfoWindow popups for POIs
 * ✅ Highlights active POI with blue icon
 * ✅ Fully interactive map with zoom and pan
 */

import React, { useCallback, useRef, useState, useMemo } from "react";
import {
  GoogleMap,
  Marker,
  Polyline,
  InfoWindow,
  useJsApiLoader,
} from "@react-google-maps/api";
import polylineDecode from "@mapbox/polyline";

import type { POI } from "@/types/POI";

// ----------------------
// 🔧 Type Definitions
// ----------------------

type POIBlock = Pick<POI, "id" | "name" | "lat" | "lng">;

interface RouteBlock {
  type: "Transportation";
  from_id: string;
  to_id: string;
  polyline: string;
}

interface Props {
  mapBlocks: (POIBlock | RouteBlock)[];
  activeId?: string;
  onSelectPOI?: (id?: string) => void;
}

const containerStyle = {
  width: "100%",
  height: "500px",
};

// ----------------------
// 🌍 Main Map Component
// ----------------------

export default function MapPanel({ mapBlocks, activeId, onSelectPOI }: Props) {
  const { isLoaded, loadError } = useJsApiLoader({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY || "",
  });

  const mapRef = useRef<google.maps.Map | null>(null);
  const [selectedPOI, setSelectedPOI] = useState<POIBlock | null>(null);

  const onLoad = useCallback((map: google.maps.Map) => {
    mapRef.current = map;
  }, []);

  const defaultCenter = useMemo(() => {
    const poi = mapBlocks.find((b): b is POIBlock => "lat" in b && "lng" in b);
    return poi
      ? { lat: poi.lat, lng: poi.lng }
      : { lat: 40.7128, lng: -74.006 };
  }, [mapBlocks]);

  if (loadError) {
    return (
      <div className="text-red-500 text-sm">
        ❌ Failed to load Google Maps. Please check your API key.
      </div>
    );
  }

  if (!isLoaded) {
    return <div className="text-gray-500 text-sm">Loading map...</div>;
  }

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={defaultCenter}
      zoom={12}
      onLoad={onLoad}
    >
      {mapBlocks.map((block) =>
        "lat" in block && "lng" in block ? (
          <Marker
            key={block.id}
            position={{ lat: block.lat, lng: block.lng }}
            onClick={() => {
              setSelectedPOI(block);
              onSelectPOI?.(block.id);
            }}
            icon={
              block.id === activeId
                ? {
                    url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
                  }
                : undefined
            }
          />
        ) : null
      )}

      {selectedPOI && (
        <InfoWindow
          position={{ lat: selectedPOI.lat, lng: selectedPOI.lng }}
          onCloseClick={() => setSelectedPOI(null)}
        >
          <div>
            <strong>{selectedPOI.name}</strong>
          </div>
        </InfoWindow>
      )}

      {mapBlocks.map((block, idx) => {
        if ("polyline" in block) {
          try {
            const path = polylineDecode
              .decode(block.polyline)
              .map(([lat, lng]) => ({ lat, lng }));
            return (
              <Polyline
                key={idx}
                path={path}
                options={{
                  strokeColor: "#ff4f81",
                  strokeOpacity: 0.9,
                  strokeWeight: 4,
                }}
              />
            );
          } catch (err) {
            console.warn(`❌ Invalid polyline at index ${idx}`, err);
            return null;
          }
        }
        return null;
      })}
    </GoogleMap>
  );
}

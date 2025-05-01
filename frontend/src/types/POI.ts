/**
 * POI.ts · Tripllery v3 Unified POI Type
 *
 * Standardized structure of a Point of Interest card.
 * Used in:
 * - Recommendation card display (POICard)
 * - Selection memory (SelectedPanel)
 * - Timeline + Preview mapping
 * - Plan backend communication
 */

export interface POI {
  id: string; // Unique POI ID, e.g. "poi_abc123"
  name: string; // Name of the POI (title)
  city?: string; // Optional: City name (for grouping / display)

  description: string; // Description summary from LLM (100–300 chars)
  rating?: number; // Optional: Google rating (1.0–5.0)

  lat: number; // Latitude
  lng: number; // Longitude

  image_url?: string; // Optional image for visual display
  highlight_tags?: string[]; // Optional tags from user reviews / LLM

  opening_hours?: string[]; // Optional: Daily hours, formatted text

  source?: {
    google_maps_url?: string; // Optional: Link to Google Maps
    review_links?: string[]; // Optional: External review links (e.g. xiaohongshu)
  };
}

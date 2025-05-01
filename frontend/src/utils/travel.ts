/**
 * getMinRequiredPOIs.ts · Tripllery v3 Travel Utils
 *
 * Calculate the minimum number of POIs required based on:
 * - Total trip duration (start_date → end_date)
 * - Selected travel intensity (chill / normal / intense)
 *
 * Used in:
 * - RecommendPage (to enforce minimum POI selection)
 * - Any step that relies on travel duration estimation
 *
 * Params:
 * -------
 * - start_datetime (string): ISO date (e.g. "2025-04-04")
 * - end_datetime (string): ISO date (e.g. "2025-04-07")
 * - intensity (string): travel style, default = "normal"
 *
 * Returns:
 * --------
 * - number: minimum number of POIs required
 */

export function getMinRequiredPOIs(
  start_datetime: string,
  end_datetime: string,
  intensity: "chill" | "normal" | "intense" = "normal"
): number {
  try {
    const start = new Date(start_datetime);
    const end = new Date(end_datetime);

    // ⏱️ Calculate number of trip days (inclusive)
    const diffInMs = end.getTime() - start.getTime();
    const tripDays =
      Math.max(1, Math.ceil(diffInMs / (1000 * 60 * 60 * 24))) + 1;

    // 🎯 Return POI count based on intensity
    switch (intensity) {
      case "chill":
        return tripDays * 1;
      case "intense":
        return tripDays * 3;
      default:
        return tripDays * 2;
    }
  } catch (err) {
    console.warn("⚠️ Invalid datetime input in getMinRequiredPOIs:", err);
    return 3; // 🛟 Fallback value in case of parsing failure
  }
}

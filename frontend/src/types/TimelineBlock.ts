/**
 * TimelineBlock defines the structure of a single activity or route block
 * in the generated daily schedule, used across preview components.
 */
export interface TimelineBlock {
  id?: string; // Optional unique identifier (e.g., for POIs)

  day: string; // The date this block belongs to (formatted as "YYYY-MM-DD")

  start_time: string; // Start time in "HH:MM" format
  end_time: string; // End time in "HH:MM" format

  activity: string; // Name or description of the activity
  type: string; // Type of block: "Sightseeing", "Meal", "Transportation", etc.

  location?: {
    lat: number;
    lng: number;
  }; // Main location of this activity (for POIs)

  from_id?: string; // ID of the starting POI (used for route blocks)
  to_id?: string; // ID of the ending POI (used for route blocks)

  from_location?: {
    lat: number;
    lng: number;
  }; // Coordinates of route start point

  to_location?: {
    lat: number;
    lng: number;
  }; // Coordinates of route end point

  polyline?: string; // Encoded polyline string for transportation route
}

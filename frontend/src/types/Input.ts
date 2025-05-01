/**
 * FormData.ts · Tripllery v3 User Input Type
 *
 * Defines the full structure of the travel form submission.
 * This type is used across:
 * - DesignForm.tsx
 * - /recommend → backend payload
 * - navigation state → RecommendPage, PlanPage, etc.
 */

export interface MealOptions {
  include_breakfast: boolean;
  include_lunch: boolean;
  include_dinner: boolean;
}

export interface FormData {
  // 📍 Basic travel info
  from: string; // Departure city (e.g. "Boston")
  to: string; // Destination city (e.g. "New York")
  date: string; // Start date of the trip (YYYY-MM-DD)
  end_date: string; // End date of the trip (YYYY-MM-DD)

  // 💬 Optional trip vibe
  description?: string; // User-described preferences / travel mood

  // 🚗 Logistics
  transportation: string; // "car" | "public"
  travelers?: number; // Optional number of travelers
  budget?: string; // Optional budget (USD)
  round_trip: boolean; // Whether return trip is needed
  include_hotels: boolean; // Whether to include hotel suggestions

  // 🍴 Meals
  meal_options: MealOptions; // Checkbox switches for breakfast/lunch/dinner

  // 🧭 Intensity of the itinerary
  intensity: "chill" | "normal" | "intense";

  // ⏰ Daily rhythm preferences
  wake_up_time?: string; // e.g. "08:00"
  return_time?: string; // e.g. "21:30"
}

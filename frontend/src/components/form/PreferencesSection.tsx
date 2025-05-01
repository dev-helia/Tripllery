import React from "react";
import { UseFormRegister, FieldErrors, UseFormWatch } from "react-hook-form";
import { FormData } from "@/types/Input";
import InfoTooltip from "./InfoTooltip";

interface PreferencesSectionProps {
  register: UseFormRegister<FormData>;
  errors: FieldErrors<FormData>;
  watch: UseFormWatch<FormData>;
}

/**
 * 🎨 PreferencesSection.tsx
 *
 * User input for:
 * - Travel style (description)
 * - Meal options
 * - Trip intensity
 */
export default function PreferencesSection({
  register,
  errors,
  watch,
}: PreferencesSectionProps) {
  const description = watch("description") || "";

  return (
    <div>
      <h2 className="text-lg font-semibold border-b pb-1 mb-4">Preferences</h2>

      {/* ✏️ Trip Description */}
      <div className="mb-4">
        <label className="flex items-center font-medium mb-1">
          Travel Style
          <InfoTooltip message="Describe your vibe or what you'd like to explore! Optional." />
        </label>
        <textarea
          {...register("description", {
            maxLength: { value: 300, message: "Max 300 characters" },
          })}
          rows={3}
          className="w-full border px-3 py-2 rounded resize-none"
        />
        <div className="text-sm text-gray-500 mt-1">
          {description.length}/300 characters
        </div>
        {errors.description && (
          <p className="text-sm text-red-500 mt-1">
            {errors.description.message}
          </p>
        )}
      </div>

      {/* 🍽️ Meal Preferences */}
      <div className="mb-4">
        <label className="block font-medium mb-2">
          Meal Options
          <InfoTooltip message="Choose which meals to include in your plan 🍱" />
        </label>
        <div className="space-y-2">
          {["breakfast", "lunch", "dinner"].map((meal) => (
            <label key={meal} className="flex items-center space-x-2">
              <input
                type="checkbox"
                {...register(`meal_options.include_${meal}` as const)}
                className="accent-pink-500"
              />
              <span className="capitalize">{meal}</span>
            </label>
          ))}
        </div>
      </div>

      {/* ⚡ Intensity Selection */}
      <div className="mb-4">
        <label className="block font-medium mb-1">
          Trip Intensity
          <InfoTooltip message="How packed do you want your daily schedule to be?" />
        </label>
        <select
          {...register("intensity", { required: "Trip intensity is required" })}
          className="w-full border px-3 py-2 rounded"
        >
          <option value="chill">🌿 Chill (1–2 POIs/day)</option>
          <option value="normal">🌤 Normal (2–3 POIs/day)</option>
          <option value="intense">⚡ Intense (3–5 POIs/day)</option>
        </select>
        {errors.intensity && (
          <p className="text-sm text-red-500 mt-1">
            {errors.intensity.message}
          </p>
        )}
      </div>
    </div>
  );
}

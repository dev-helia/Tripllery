import React from "react";
import { UseFormRegister, FieldErrors } from "react-hook-form";
import { FormData } from "@/types/Input";
import InfoTooltip from "./InfoTooltip";

interface TravelInfoSectionProps {
  register: UseFormRegister<FormData>;
  errors: FieldErrors<FormData>;
}

/**
 * 🗺️ TravelInfoSection.tsx
 *
 * Collects departure, destination, and trip dates.
 */
export default function TravelInfoSection({
  register,
  errors,
}: TravelInfoSectionProps) {
  return (
    <div>
      <h2 className="text-lg font-semibold border-b pb-1 mb-4">Travel Info</h2>

      {/* 🛫 From */}
      <div className="mb-4">
        <label className="flex items-center font-medium mb-1">
          From
          <InfoTooltip message="Your departure city (e.g. Boston)" />
        </label>
        <input
          {...register("from", { required: "Required" })}
          placeholder="e.g. Boston"
          className="w-full border px-3 py-2 rounded"
        />
        {errors.from && (
          <p className="text-sm text-red-500 mt-1">{errors.from.message}</p>
        )}
      </div>

      {/* 🛬 To */}
      <div className="mb-4">
        <label className="flex items-center font-medium mb-1">
          To
          <InfoTooltip message="Your destination city (e.g. New York)" />
        </label>
        <input
          {...register("to", { required: "Required" })}
          placeholder="e.g. New York"
          className="w-full border px-3 py-2 rounded"
        />
        {errors.to && (
          <p className="text-sm text-red-500 mt-1">{errors.to.message}</p>
        )}
      </div>

      {/* 📅 Dates */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        {/* Start Date */}
        <div>
          <label className="flex items-center font-medium mb-1">
            Start Date
            <InfoTooltip message="Start of your trip" />
          </label>
          <input
            type="date"
            {...register("date", { required: "Required" })}
            className="w-full border px-3 py-2 rounded"
          />
          {errors.date && (
            <p className="text-sm text-red-500 mt-1">{errors.date.message}</p>
          )}
        </div>

        {/* End Date */}
        <div>
          <label className="flex items-center font-medium mb-1">
            End Date
            <InfoTooltip message="End of your trip" />
          </label>
          <input
            type="date"
            {...register("end_date", { required: "Required" })}
            className="w-full border px-3 py-2 rounded"
          />
          {errors.end_date && (
            <p className="text-sm text-red-500 mt-1">
              {errors.end_date.message}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

import React from "react";
import { UseFormRegister } from "react-hook-form";
import { FormData } from "@/types/Input"; // ✅ 使用统一 FormData 类型

interface FlagsSectionProps {
  register: UseFormRegister<FormData>;
}

/**
 * 🏳️‍🌈 FlagsSection.tsx
 *
 * This section renders toggleable checkboxes for:
 * - Whether the trip is a round trip
 * - Whether to include hotels in the plan
 *
 * Props:
 * ------
 * - register: hook-form's register function for controlled inputs
 */
export default function FlagsSection({ register }: FlagsSectionProps) {
  return (
    <div className="flex items-center space-x-4 mt-4">
      {/* 🔁 Round Trip Toggle */}
      <label className="flex items-center space-x-2">
        <input
          type="checkbox"
          {...register("round_trip")}
          className="accent-pink-500"
        />
        <span>Round Trip</span>
      </label>

      {/* 🏨 Include Hotels Toggle */}
      <label className="flex items-center space-x-2">
        <input
          type="checkbox"
          {...register("include_hotels")}
          className="accent-pink-500"
        />
        <span>Include Hotels</span>
      </label>
    </div>
  );
}

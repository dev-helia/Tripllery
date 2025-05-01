import React from "react";
import { UseFormRegister, FieldErrors } from "react-hook-form";
import { FormData } from "@/types/Input"; // ✅ 统一使用你的 Input.ts 路径！

interface LogisticsSectionProps {
  register: UseFormRegister<FormData>;
  errors: FieldErrors<FormData>;
}

/**
 * 🧳 LogisticsSection.tsx
 *
 * Inputs for:
 * - Transportation mode
 * - Travelers count
 * - Budget
 * - Wake-up & Return time
 */
export default function LogisticsSection({
  register,
  errors,
}: LogisticsSectionProps) {
  return (
    <>
      {/* 🚗 Transportation */}
      <div className="mb-4">
        <label className="block font-medium mb-1">Transportation</label>
        <select
          {...register("transportation")}
          className="w-full border px-3 py-2 rounded"
        >
          <option value="car">Car</option>
          <option value="public">Public Transport</option>
        </select>
      </div>

      {/* 👥 Travelers */}
      <div className="mb-4">
        <label className="block font-medium mb-1">Travelers</label>
        <input
          type="number"
          {...register("travelers")}
          placeholder="e.g. 2"
          min={1}
          className="w-full border px-3 py-2 rounded"
        />
        {errors.travelers && (
          <p className="text-sm text-red-500 mt-1">
            {errors.travelers.message}
          </p>
        )}
      </div>

      {/* 💰 Budget */}
      <div className="mb-4">
        <label className="block font-medium mb-1">Budget (USD)</label>
        <input
          type="number"
          {...register("budget")}
          placeholder="Optional"
          className="w-full border px-3 py-2 rounded"
        />
        {errors.budget && (
          <p className="text-sm text-red-500 mt-1">{errors.budget.message}</p>
        )}
      </div>

      {/* 🕗 Wake-up Time */}
      <div className="mb-4">
        <label className="block font-medium mb-1">Wake-up Time</label>
        <input
          type="time"
          {...register("wake_up_time")}
          className="w-full border px-3 py-2 rounded"
        />
      </div>

      {/* 🌙 Return Hotel Time */}
      <div className="mb-4">
        <label className="block font-medium mb-1">Return Hotel Time</label>
        <input
          type="time"
          {...register("return_time")}
          className="w-full border px-3 py-2 rounded"
        />
      </div>
    </>
  );
}

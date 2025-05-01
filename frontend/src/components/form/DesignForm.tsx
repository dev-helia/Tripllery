import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { FormData } from "@/types/Input"; // ✅ 用 Input.ts 路径引用类型
import { navigateWithPayload } from "@/utils/navigateWithPayload"; // ✅ 封装跳转方法

// 🧩 子表单区域组件
import TravelInfoSection from "./TravelInfoSection";
import PreferencesSection from "./PreferencesSection";
import LogisticsSection from "./LogisticsSection";
import FlagsSection from "./FlagsSection";

// 🎛️ 按钮和加载组件
import SubmitButton from "./SubmitButton";
import LoadingAnimation from "./LoadingAnimation";

export default function DesignForm(): JSX.Element {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    watch,
    setError,
    clearErrors,
  } = useForm<FormData>({
    defaultValues: {
      meal_options: {
        include_breakfast: true,
        include_lunch: true,
        include_dinner: true,
      },
      round_trip: false,
      include_hotels: false,
      intensity: "normal",
    },
  });

  const navigate = useNavigate();
  const startDate = watch("date");
  const endDate = watch("end_date");

  useEffect(() => {
    if (startDate && endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      if (start > end) {
        setError("end_date", {
          type: "manual",
          message: "End date must be after start date",
        });
      } else {
        clearErrors("end_date");
      }
    }
  }, [startDate, endDate, setError, clearErrors]);

  const onSubmit = async (data: FormData) => {
    const payload = {
      departure_city: data.from,
      destination: data.to,
      start_datetime: data.date,
      end_datetime: data.end_date,
      trip_preferences: data.description || "",
      transportation: data.transportation,
      travelers: data.travelers,
      budget: data.budget,
      round_trip: data.round_trip,
      include_hotels: data.include_hotels,
      meal_options: data.meal_options,
      intensity: data.intensity,
      wake_up_time: data.wake_up_time || "",
      return_time: data.return_time || "",
    };

    // 🧪 Debug log
    console.log("🧾 Final payload:", payload);

    try {
      const res = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Server error");

      const result = await res.json();

      // ✅ 封装跳转
      navigateWithPayload(navigate, "/recommend", {
        formData: payload,
        cards: result.cards,
        all_pois: result.all_pois,
      });
    } catch (err) {
      console.error("Submit failed:", err);
    }
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="max-w-xl mx-auto p-6 space-y-10 text-gray-800"
    >
      <TravelInfoSection register={register} errors={errors} />
      <PreferencesSection register={register} errors={errors} watch={watch} />
      <LogisticsSection register={register} errors={errors} />
      <FlagsSection register={register} />
      <div className="pt-4">
        {isSubmitting ? <LoadingAnimation /> : <SubmitButton />}
      </div>
    </form>
  );
}

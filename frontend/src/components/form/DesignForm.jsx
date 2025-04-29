import React from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import InfoTooltip from "./InfoTooltip";
import SubmitButton from "./SubmitButton";
import LoadingAnimation from "./LoadingAnimation";
// todo ??????????????????
export default function DesignForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    try {
      const res = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const result = await res.json();
      // 保存推荐结果 or 跳转
      navigate("/recommend");
    } catch (err) {
      console.error("提交失败:", err);
    }
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="max-w-xl mx-auto p-6 space-y-6"
    >
      <div>
        <label className="flex items-center font-medium mb-1">
          出发地
          <InfoTooltip message="你现在的位置或出发城市" />
        </label>
        <input
          {...register("from", { required: "出发地不能为空" })}
          className="w-full border px-3 py-2 rounded"
        />
        {errors.from && (
          <p className="text-red-500 text-sm">{errors.from.message}</p>
        )}
      </div>

      <div>
        <label className="flex items-center font-medium mb-1">
          目的地
          <InfoTooltip message="你想要去的地方城市" />
        </label>
        <input
          {...register("to", { required: "目的地不能为空" })}
          className="w-full border px-3 py-2 rounded"
        />
        {errors.to && (
          <p className="text-red-500 text-sm">{errors.to.message}</p>
        )}
      </div>

      <div>
        <label className="flex items-center font-medium mb-1">
          出发日期
          <InfoTooltip message="你希望旅行开始的日期" />
        </label>
        <input
          type="date"
          {...register("date", { required: "出发日期不能为空" })}
          className="w-full border px-3 py-2 rounded"
        />
        {errors.date && (
          <p className="text-red-500 text-sm">{errors.date.message}</p>
        )}
      </div>

      <div>
        <label className="flex items-center font-medium mb-1">
          旅行风格描述
          <InfoTooltip message="你对这次旅程的期待，比如放松、文化、美食…" />
        </label>
        <textarea
          {...register("description", { required: "描述不能为空" })}
          rows={3}
          className="w-full border px-3 py-2 rounded"
        />
        {errors.description && (
          <p className="text-red-500 text-sm">{errors.description.message}</p>
        )}
      </div>

      <div className="pt-4">
        {isSubmitting ? <LoadingAnimation /> : <SubmitButton />}
      </div>
    </form>
  );
}

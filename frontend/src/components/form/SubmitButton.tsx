import React from "react";

interface SubmitButtonProps {
  label?: string;
  disabled?: boolean;
}

const SubmitButton: React.FC<SubmitButtonProps> = ({
  label = "Start Recommendation →",
  disabled = false,
}) => {
  return (
    <button
      type="submit"
      disabled={disabled}
      className={`w-full py-3 font-bold rounded transition text-white ${
        disabled
          ? "bg-gray-300 cursor-not-allowed"
          : "bg-pink-600 hover:bg-pink-700"
      }`}
    >
      {label}
    </button>
  );
};

export default SubmitButton;

import React from "react";

interface LoadingAnimationProps {
  message?: string;
}

/**
 * 🌸 LoadingAnimation.tsx
 *
 * Shows a spinning loader + optional message.
 *
 * Props:
 * -------
 * - message: Custom text, defaults to "Generating recommendation..."
 */
export default function LoadingAnimation({
  message = "Generating recommendation...",
}: LoadingAnimationProps) {
  return (
    <div className="flex flex-col items-center justify-center text-center text-sm text-gray-600 space-y-2 py-6">
      {/* 🎡 Spinner */}
      <div className="w-8 h-8 border-4 border-pink-300 border-t-transparent rounded-full animate-spin"></div>

      {/* 📝 Message */}
      <div>{message}</div>
    </div>
  );
}

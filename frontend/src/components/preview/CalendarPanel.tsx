/**
 * CalendarPanel.tsx · Tripllery v3 Preview Date Selector
 *
 * Renders an interactive calendar panel for previewing trip days.
 * Allows switching months, selecting specific days, and highlights Day X of Y.
 *
 * Props:
 * -------
 * - startDate (string): trip start date (ISO format)
 * - endDate (string): trip end date (ISO format)
 * - selectedDate (string): currently selected day
 * - onSelect (function): callback triggered on date selection
 *
 * Features:
 * ---------
 * ✅ Scrollable calendar month view
 * ✅ Highlights today, selected date, and trip days
 * ✅ Shows Day X of Y
 * ✅ "Back to Day 1" quick return button
 */

import React, { useState } from "react";
import dayjs from "dayjs";
import classNames from "classnames";
import { useMonthlyCalendarRange } from "../../hooks/useMonthlyCalendarRange";

interface CalendarPanelProps {
  startDate: string;
  endDate: string;
  selectedDate: string;
  onSelect: (date: string) => void;
}

const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

export default function CalendarPanel({
  startDate,
  endDate,
  selectedDate,
  onSelect,
}: CalendarPanelProps) {
  const initial = dayjs(startDate || selectedDate || dayjs());
  const [currentMonth, setCurrentMonth] = useState(initial.startOf("month"));

  // ✅ 调用全局 hook 替代内部 generateMonthDates
  const dates = useMonthlyCalendarRange(
    currentMonth.format("YYYY-MM-DD"),
    currentMonth.endOf("month").format("YYYY-MM-DD")
  );

  const handleBackToStart = () => {
    const start = dayjs(startDate);
    setCurrentMonth(start.startOf("month"));
    onSelect(start.format("YYYY-MM-DD"));
  };

  const isInRange = (date: string): boolean => {
    return (
      dayjs(date).isSameOrAfter(startDate) &&
      dayjs(date).isSameOrBefore(endDate)
    );
  };

  const isDayInTrip =
    dayjs(selectedDate).isSameOrAfter(startDate) &&
    dayjs(selectedDate).isSameOrBefore(endDate);

  return (
    <div className="p-4 bg-white rounded shadow-sm space-y-3">
      {/* 📅 Month Header */}
      <div className="flex items-center justify-between mb-2">
        <button
          onClick={() => setCurrentMonth(currentMonth.subtract(1, "month"))}
          className="text-sm text-gray-600 hover:text-pink-600 px-2"
        >
          «
        </button>
        <div className="text-base font-semibold text-gray-800">
          {currentMonth.format("MMMM YYYY")}
        </div>
        <button
          onClick={() => setCurrentMonth(currentMonth.add(1, "month"))}
          className="text-sm text-gray-600 hover:text-pink-600 px-2"
        >
          »
        </button>
      </div>

      {/* 🗓️ Weekday Titles */}
      <div className="grid grid-cols-7 text-center text-xs text-gray-400 font-medium pb-1">
        {WEEKDAYS.map((day) => (
          <div key={day}>{day}</div>
        ))}
      </div>

      {/* 📆 Calendar Grid */}
      <div className="grid grid-cols-7 gap-2">
        {dates.map((date) => {
          const isSelected = date === selectedDate;
          const isToday = date === dayjs().format("YYYY-MM-DD");
          const inRange = isInRange(date);

          return (
            <button
              key={date}
              onClick={() => inRange && onSelect(date)}
              disabled={!inRange}
              className={classNames(
                "text-sm rounded-full px-2 py-1 transition",
                {
                  "bg-indigo-600 text-white font-bold": isSelected,
                  "bg-pink-100 text-pink-600":
                    isToday && !isSelected && inRange,
                  "hover:bg-indigo-100 text-gray-700":
                    inRange && !isSelected && !isToday,
                  "text-gray-300 cursor-not-allowed": !inRange,
                }
              )}
            >
              {dayjs(date).format("D")}
            </button>
          );
        })}
      </div>

      {/* 🎯 Footer: Return + Day X Info */}
      <div className="text-center pt-2 space-y-1">
        <button
          onClick={handleBackToStart}
          className="text-xs text-indigo-600 hover:underline"
        >
          Back to Day 1
        </button>

        {isDayInTrip && (
          <div className="text-xs text-gray-500">
            Day {dayjs(selectedDate).diff(dayjs(startDate), "day") + 1} of{" "}
            {dayjs(endDate).diff(dayjs(startDate), "day") + 1}
          </div>
        )}
      </div>
    </div>
  );
}

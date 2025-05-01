/**
 * useMonthlyCalendarRange.ts · Tripllery v3 Preview Helper
 *
 * This hook generates a list of all dates (YYYY-MM-DD) between the full months
 * that cover the startDate and endDate.
 *
 * Use case:
 * ---------
 * - To render a continuous calendar grid across trip span
 * - Ensures the first and last month are fully shown
 *
 * Params:
 * -------
 * - startDate: string (e.g. "2025-04-04")
 * - endDate: string (e.g. "2025-04-07")
 *
 * Returns:
 * -------
 * - string[] of date strings for full month span
 */

import dayjs from "dayjs";

export const useMonthlyCalendarRange = (
  startDate: string,
  endDate: string
): string[] => {
  const start = dayjs(startDate).startOf("month");
  const end = dayjs(endDate).endOf("month");

  const days: string[] = [];
  let current = start;

  while (current.isBefore(end) || current.isSame(end, "day")) {
    days.push(current.format("YYYY-MM-DD"));
    current = current.add(1, "day");
  }

  return days;
};

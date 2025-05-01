/**
 * navigateWithPayload.ts · Tripllery v3 Routing Helper
 *
 * A single helper to move complex state (formData + POI / plan meta)
 * from one page to another. Call this instead of raw `navigate(...)`.
 *
 * Used in
 * ── DesignForm  ➝  /recommend
 * ── Recommend   ➝  /plan
 * ── Plan        ➝  /preview  (next step)
 */

import { NavigateFunction } from "react-router-dom";

/* ---------- Unified payload type ---------- */
export interface NavPayload {
  /* original form body  */
  formData: any;

  /* ↓↓↓ depending on the stage, only one或多字段会用到 ↓↓↓ */
  cards?: any[]; // /recommend response – small list
  all_pois?: any[]; // full POI pool – for /plan
  accepted_pois?: string[]; // selected ids – for /plan
  plan?: any; // plan split by day – for /preview
  options?: any; // extra options – for /preview

  /* allow future extension */
  [key: string]: any;
}

/* ---------- Helper ---------- */
export function navigateWithPayload(
  navigate: NavigateFunction,
  path: string,
  payload: NavPayload
): void {
  /* ensure the two array fields are never undefined –> easier for receivers */
  const {
    cards = [],
    all_pois = [],
    ...rest // formData, accepted_pois, plan, options, etc.
  } = payload;

  navigate(path, {
    state: {
      /* default-filled arrays */
      cards,
      all_pois,

      /* everything else – one shot */
      ...rest,
    },
  });
}

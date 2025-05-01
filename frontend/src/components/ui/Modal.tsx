/**
 * Modal.tsx · Tripllery v3 UI Component
 *
 * A lightweight, reusable **modal dialog / overlay** component.
 * It is rendered **portal-style** (fixed to the viewport) and blocks
 * interaction with the page until the user closes it.
 *
 * Usage
 * ------
 * ```tsx
 * const [show, setShow] = useState(false);
 *
 * {show && (
 *   <Modal onClose={() => setShow(false)}>
 *     <POICard poi={selectedPoi} />
 *   </Modal>
 * )}
 * ```
 *
 * Props
 * -----
 * • `children`  ReactNode – whatever should appear inside the dialog
 * • `onClose()` function – called when the user clicks the ✕ button
 *   **or** anywhere on the dark backdrop
 *
 * Design decisions
 * ----------------
 * • **Backdrop click closes** – quick way to dismiss
 * • `stopPropagation()` on the inner panel prevents accidental close when
 *   interacting with the content.
 * • `z-50` (Tailwind) keeps it above every other layer in the app.
 */

import React, { ReactNode } from "react";

export default function Modal({
  children,
  onClose,
}: {
  children: ReactNode;
  onClose: () => void;
}) {
  return (
    /* 🔲 Backdrop: dark translucent layer that fills the viewport */
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      onClick={onClose} // ➡️ click outside = close
    >
      {/* 🗔 Dialog panel */}
      <div
        className="bg-white rounded-lg shadow-xl max-w-md w-[90%] p-4"
        onClick={(e) => e.stopPropagation()} // ⛔ stop bubbling
      >
        {/* ✕ Close button */}
        <button
          className="ml-auto mb-2 text-gray-400 hover:text-gray-600 text-xl leading-none"
          onClick={onClose}
          aria-label="Close modal"
        >
          ×
        </button>

        {/* 📦 Modal content injected by parent */}
        {children}
      </div>
    </div>
  );
}

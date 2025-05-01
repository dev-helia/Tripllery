/**
 * Navbar.tsx · Tripllery Global Top Navigation Bar
 *
 * This component renders a simple transparent navbar
 * that sits on top of the landing page or other full-screen content.
 *
 * Features:
 * ---------
 * ✅ Brand logo or name on the left
 * ✅ "Login" button on the right (currently static)
 * ✅ Absolute positioning with `pointer-events` logic for layering
 *
 * Usage:
 * ------
 * Usually placed at the top of pages like `LandingPage`
 * Can be expanded later to support navigation links, user menu, etc.
 */

import React from "react";

const Navbar: React.FC = () => {
  return (
    <header
      className="
        w-full px-6 py-4 flex justify-between items-center
        bg-transparent absolute top-0 z-20
        pointer-events-none
      "
    >
      {/* 🔠 Brand Name */}
      <h1 className="text-2xl font-bold tracking-wider">CardTrip</h1>

      {/* 🔒 Login Button (future: link to auth) */}
      <button
        className="
          text-white text-sm border border-white px-4 py-2 rounded-full
          hover:bg-white hover:text-black transition
          pointer-events-auto
        "
      >
        Logout
      </button>
    </header>
  );
};

export default Navbar;

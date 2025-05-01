/**
 * DesignPage.tsx · Tripllery v3 Journey Form Page
 *
 * Entry page for users to customize their trip preferences.
 * It contains the form with travel inputs (from, to, dates, preferences...).
 *
 * Features:
 * ---------
 * ✅ Loads the top navbar
 * ✅ Renders the <DesignForm /> component
 * ✅ Applies basic page styling (padding, centered width)
 *
 * Routes:
 * -------
 * - This is mounted at `/design` route via React Router.
 */

import React from "react";
import DesignForm from "../components/form/DesignForm";
import Navbar from "../components/layout/Navbar";

export default function DesignPage() {
  return (
    <div className="min-h-screen bg-white text-gray-800">
      {/* ⛳ Top navbar */}
      <Navbar />

      {/* 📋 Main form layout */}
      <main className="max-w-3xl mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold mb-8 text-center">
          Customize your journey
        </h1>

        {/* 🚀 Render the form component */}
        <DesignForm />
      </main>
    </div>
  );
}

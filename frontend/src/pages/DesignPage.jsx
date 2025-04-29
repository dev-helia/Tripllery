import React from "react";
import DesignForm from "../components/form/DesignForm";
import Navbar from "../components/Navbar";

export default function DesignPage() {
  return (
    <div className="min-h-screen bg-white text-gray-800">
      <Navbar />
      <main className="max-w-3xl mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold mb-8 text-center">
          Customize your journey
        </h1>
        <DesignForm />
      </main>
    </div>
  );
}

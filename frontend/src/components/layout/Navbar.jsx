import React from "react";

export default function Navbar() {
  return (
    <header className="w-full px-6 py-4 flex justify-between items-center bg-transparent absolute top-0 z-20">
      <h1 className="text-2xl font-bold tracking-wider">Tripllery</h1>
      <button className="text-white text-sm border border-white px-4 py-2 rounded-full hover:bg-white hover:text-black transition">
        Login
      </button>
    </header>
  );
}

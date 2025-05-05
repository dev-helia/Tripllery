import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";
import rollupNodePolyFill from "rollup-plugin-polyfill-node";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
      crypto: "crypto-browserify",
      stream: "stream-browserify",
      buffer: "buffer",
    },
  },
  define: {
    global: "globalThis",
  },
  server: {
    proxy: {
      "/recommend": "http://localhost:5001",
      "/plan": "http://localhost:5001",
      "/preview": "http://localhost:5001",
    },
  },
  optimizeDeps: {
    include: ["crypto-browserify", "stream-browserify", "buffer"],
  },
  build: {
    rollupOptions: {
      plugins: [rollupNodePolyFill()],
    },
  },
});

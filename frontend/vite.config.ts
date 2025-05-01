import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  plugins: [react()], // 💥 这里就保留 react，别加别的
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  server: {
    proxy: {
      "/recommend": "http://localhost:5001",
      "/plan": "http://localhost:5001",
      "/preview": "http://localhost:5001",
    },
  },
});

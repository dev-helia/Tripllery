/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html", // 扫描根目录 HTML 文件
    "./src/**/*.{js,ts,jsx,tsx}", // 扫描 src 目录下的所有 JS/TS/React 文件
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

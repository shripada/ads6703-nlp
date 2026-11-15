import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Locally, /api/... goes to the FastAPI server on port 8000. On Vercel, vercel.json does the same job.
export default defineConfig({
  plugins: [react()],
  server: { proxy: { "/api": "http://localhost:8000" } },
});

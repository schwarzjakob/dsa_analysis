import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/dsa4": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
      },
      "/dsa5": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
      },
    },
  },
});

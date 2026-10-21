import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes("node_modules")) return undefined;
          if (/node_modules\/(react|react-dom|react-router|scheduler)\//.test(id)) return "react-vendor";
          if (id.includes("node_modules/framer-motion/")) return "animation-vendor";
          if (id.includes("node_modules/lucide-react/")) return "icon-vendor";
          return undefined;
        },
      },
    },
  },
  server: {
    port: 5173,
  },
});

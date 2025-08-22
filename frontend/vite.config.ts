import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  optimizeDeps: {
    exclude: ['cesium']
  },
  build: {
    rollupOptions: {
      // Remove the manualChunks for cesium since it's likely being externalized
      external: [], // Ensure no modules are externalized
      output: {
        // You can keep other manualChunks but remove cesium
        manualChunks: (id) => {
          if (id.includes('node_modules')) {
            // Group other node_modules but exclude cesium
            if (id.includes('cesium')) {
              return undefined; // Let Rollup handle cesium normally
            }
            return 'vendor';
          }
        }
      }
    }
  },
  server: {
    fs: {
      allow: ['..'] // Allow access to parent directories if needed
    }
  }
});
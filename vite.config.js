import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Relative URLs keep the built site working on GitHub Pages project URLs
// (for example: https://username.github.io/repository/).
export default defineConfig({
  base: './',
  plugins: [react()],
});

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#090d16',
        card: '#111726',
        border: '#1f293d',
        primary: {
          DEFAULT: '#6366f1',
          foreground: '#ffffff',
        },
        accent: {
          DEFAULT: '#10b981',
          foreground: '#ffffff',
        },
      },
    },
  },
  plugins: [],
};

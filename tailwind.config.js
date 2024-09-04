/** @type {import('tailwindcss').Config} */
// tailwind.config.js
module.exports = {
  content: [
    './app/templates/**/*.html', // All HTML files in the templates directory
    './app/static/js/**/*.js',    // If you have JS files using Tailwind classes
    './app/**/*.py',              // If you are using classes in Python files
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
};





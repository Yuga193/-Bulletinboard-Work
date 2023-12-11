/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html", "./app/static/src/**/*.js"],
  theme: {
    extend: {
      backgroundColor: {
        'header': '#050081',
      },
      opacity: {
        '50': '0.5',
      },
    },
  },
  plugins: [],
};

/** @type {import('next').NextConfig} */
const nextConfig = {
  allowedDevOrigins: [
    "http://localhost:3000",
    "http://192.168.0.37:3000",
    "http://163.47.70.74:3000",
  ],
};
module.exports = { output: 'standalone' };
module.exports = nextConfig;
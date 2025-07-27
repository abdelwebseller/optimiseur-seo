import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  experimental: {
    outputFileTracingRoot: undefined,
  },
  // Désactiver la télémetrie
  telemetry: false,
};

export default nextConfig;

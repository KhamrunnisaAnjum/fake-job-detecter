import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  turbopack: {
    root: path.resolve(__dirname),
  },
<<<<<<< HEAD
=======
  devIndicators: {
    appIsrStatus: false,
    buildActivity: false,
  },
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6
};

export default nextConfig;
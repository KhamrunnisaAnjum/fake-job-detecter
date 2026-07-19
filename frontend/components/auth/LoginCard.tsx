"use client";

import { useState } from "react";
import { FcGoogle } from "react-icons/fc";
import {
  FiMail,
  FiLock,
  FiEye,
  FiEyeOff,
  FiArrowRight,
  FiShield,
} from "react-icons/fi";

export default function LoginCard() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="flex h-full flex-col justify-center bg-[#0F0F10] px-24">
      {/* Logo */}

      <div className="mb-16">
        <h2 className="text-3xl font-semibold tracking-tight text-white">
          Job<span className="text-neutral-500">X</span>
        </h2>
      </div>

      {/* Heading */}

      <h1 className="text-5xl font-semibold tracking-tight text-white">
        Welcome back
      </h1>

      <p className="mt-4 text-lg text-neutral-400">
        Sign in to continue to your account.
      </p>

      {/* Google */}

      <button className="mt-12 flex h-14 w-full items-center justify-center gap-3 rounded-2xl border border-neutral-800 bg-transparent text-white transition-all duration-300 hover:border-neutral-600 hover:bg-neutral-900">
        <FcGoogle size={22} />
        <span className="font-medium">Continue with Google</span>
      </button>

      {/* Divider */}

      <div className="my-8 flex items-center gap-4">
        <div className="h-px flex-1 bg-neutral-800" />

        <span className="text-sm text-neutral-500">or continue with email</span>

        <div className="h-px flex-1 bg-neutral-800" />
      </div>

      {/* Secure */}

      <div className="mb-6 flex items-center gap-2 text-sm text-neutral-500">
        <FiShield size={15} />
        Secure Login
      </div>

      {/* Email */}

      <label className="mb-2 text-sm font-medium text-neutral-300">
        Email Address
      </label>

      <div className="relative mb-6">
        <FiMail
          className="absolute left-5 top-1/2 -translate-y-1/2 text-neutral-500"
          size={20}
        />

        <input
          type="email"
          placeholder="you@example.com"
          className="h-15 w-full rounded-2xl border border-neutral-800 bg-[#151515] pl-14 pr-5 text-white placeholder:text-neutral-500 outline-none transition-all duration-300 focus:border-neutral-500 focus:ring-2 focus:ring-neutral-700"
        />
      </div>

      {/* Password */}

      <label className="mb-2 text-sm font-medium text-neutral-300">
        Password
      </label>

      <div className="relative">
        <FiLock
          className="absolute left-5 top-1/2 -translate-y-1/2 text-neutral-500"
          size={20}
        />

        <input
          type={showPassword ? "text" : "password"}
          placeholder="••••••••"
          className="h-15 w-full rounded-2xl border border-neutral-800 bg-[#151515] pl-14 pr-14 text-white placeholder:text-neutral-500 outline-none transition-all duration-300 focus:border-neutral-500 focus:ring-2 focus:ring-neutral-700"
        />

        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="absolute right-5 top-1/2 -translate-y-1/2 text-neutral-500 transition hover:text-white"
        >
          {showPassword ? <FiEyeOff size={20} /> : <FiEye size={20} />}
        </button>
      </div>

      {/* Remember */}

      <div className="mt-6 flex items-center justify-between">
        <label className="flex items-center gap-2 text-sm text-neutral-400">
          <input type="checkbox" className="accent-white" />
          Remember me
        </label>

        <button className="text-sm text-neutral-400 transition hover:text-white">
          Forgot password?
        </button>
      </div>

      {/* Button */}

      <button className="mt-9 flex h-14 w-full items-center justify-center gap-2 rounded-2xl bg-white text-base font-semibold text-black shadow-lg transition-all duration-300 hover:-translate-y-0.5 hover:bg-neutral-200">
        Sign In
        <FiArrowRight />
      </button>

      {/* Footer */}

      <p className="mt-8 text-center text-sm text-neutral-500">
        Dont have an account?{" "}
        <button className="font-medium text-white transition hover:text-neutral-300">
          Create an account
        </button>
      </p>
    </div>
  );
}

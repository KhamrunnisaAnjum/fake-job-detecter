"use client";

import { useState } from "react";
import { FiMessageSquare, FiAlertCircle } from "react-icons/fi";

export default function AnalyzerPage() {
  const [loading, setLoading] = useState(false);

  const analyzeMessage = () => {
    setLoading(true);

    setTimeout(() => {
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-[#F6F7FB] p-10">
      <div className="max-w-6xl mx-auto">
        <p className="uppercase tracking-[4px] text-sm text-neutral-500">
          JobX
        </p>

        <h1 className="text-5xl font-bold mt-2">Message Analyzer</h1>

        <p className="text-neutral-500 mt-4">
          Detect fake recruiter messages, WhatsApp scams and Telegram fraud.
        </p>

        <div className="mt-10 rounded-3xl bg-white p-8 shadow-sm">
          <textarea
            rows={12}
            className="w-full rounded-2xl border p-5 outline-none focus:border-black"
            placeholder="Paste recruiter message here..."
          />

          <button
            onClick={analyzeMessage}
            className="mt-6 flex items-center gap-3 rounded-2xl bg-black px-8 py-4 text-white hover:scale-105 transition"
          >
            <FiMessageSquare />

            {loading ? "Analyzing..." : "Analyze Message"}
          </button>
        </div>

        <div className="mt-8 rounded-3xl bg-white p-8 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="rounded-full bg-red-100 p-4">
              <FiAlertCircle className="text-red-500" size={30} />
            </div>

            <div>
              <h2 className="text-3xl font-bold">Scam Probability</h2>

              <p className="text-neutral-500">96%</p>
            </div>
          </div>

          <div className="mt-8 h-4 rounded-full bg-neutral-200">
            <div className="h-4 w-[96%] rounded-full bg-red-500"></div>
          </div>

          <ul className="mt-8 space-y-3 text-neutral-600">
            <li>⚠ Payment requested before interview</li>

            <li>⚠ Telegram contact detected</li>

            <li>⚠ Unrealistic salary promise</li>

            <li>⚠ Urgent joining pressure</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

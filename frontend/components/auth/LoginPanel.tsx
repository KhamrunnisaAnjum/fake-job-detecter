
import { FiShield, FiBriefcase, FiZap } from "react-icons/fi";

export default function LoginPanel() {
  return (
    <div className="relative h-full overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-zinc-900 via-neutral-800 to-black" />

      {/* Dark Overlay */}

      <div className="absolute inset-0 bg-black/60" />

      {/* Glass Card */}

      <div className="absolute bottom-12 left-12 right-12">
        <div className="rounded-[32px] border border-white/10 bg-black/35 p-10 backdrop-blur-xl shadow-2xl">
          <p className="mb-4 text-sm font-medium tracking-[6px] text-neutral-400">
            JOBX
          </p>

          <h2 className="text-[54px] font-semibold leading-tight text-white">
            Protect Your
            <br />
            Career Journey
          </h2>

          <p className="mt-6 max-w-lg text-lg leading-8 text-neutral-300">
            Detect fake recruiters, phishing job offers and fraudulent companies
            before you apply using intelligent AI-powered analysis.
          </p>

          {/* Features */}

          <div className="mt-10 space-y-5">
            <div className="flex items-center gap-4">
              <div className="rounded-xl bg-white/10 p-2">
                <FiShield size={20} className="text-white" />
              </div>

              <span className="text-lg text-white">AI Scam Detection</span>
            </div>

            <div className="flex items-center gap-4">
              <div className="rounded-xl bg-white/10 p-2">
                <FiBriefcase size={20} className="text-white" />
              </div>

              <span className="text-lg text-white">Company Verification</span>
            </div>

            <div className="flex items-center gap-4">
              <div className="rounded-xl bg-white/10 p-2">
                <FiZap size={20} className="text-white" />
              </div>

              <span className="text-lg text-white">Instant Risk Analysis</span>
            </div>
          </div>

          {/* Stats */}

          <div className="mt-12 grid grid-cols-3 border-t border-white/10 pt-8">
            <div>
              <h3 className="text-4xl font-bold text-white">98%</h3>
              <p className="mt-1 text-neutral-400">Detection Accuracy</p>
            </div>

            <div>
              <h3 className="text-4xl font-bold text-white">15K+</h3>
              <p className="mt-1 text-neutral-400">Jobs Analyzed</p>
            </div>

            <div>
              <h3 className="text-4xl font-bold text-white">24/7</h3>
              <p className="mt-1 text-neutral-400">Protection</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

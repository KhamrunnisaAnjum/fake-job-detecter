import { FiArrowRight, FiSearch, FiClock } from "react-icons/fi";

export default function Hero() {
  return (
    <section className="mt-8 overflow-hidden rounded-[32px] bg-gradient-to-r from-black via-neutral-900 to-neutral-800 p-10 text-white shadow-xl">
      <div className="flex items-center justify-between">
        {/* Left */}

        <div className="max-w-2xl">
          <p className="mb-3 text-sm uppercase tracking-[4px] text-neutral-400">
            AI JOB SECURITY
          </p>

          <h1 className="text-5xl font-bold leading-tight">
            Protect Your Career
            <br />
            Before You Apply.
          </h1>

          <p className="mt-6 max-w-xl text-lg leading-8 text-neutral-300">
            Analyze job postings using Artificial Intelligence to detect fake
            recruiters, phishing attempts and fraudulent companies within
            seconds.
          </p>

          <div className="mt-10 flex gap-4">
            <button className="flex items-center gap-2 rounded-2xl bg-white px-7 py-4 font-semibold text-black transition hover:scale-105">
              <FiSearch />
              Scan Job
            </button>

            <button className="flex items-center gap-2 rounded-2xl border border-white/20 px-7 py-4 transition hover:bg-white/10">
              <FiClock />
              View History
            </button>
          </div>
        </div>

        {/* Right */}

        <div className="hidden lg:flex h-64 w-64 items-center justify-center rounded-full bg-white/5 backdrop-blur-xl">
          <div className="flex h-44 w-44 items-center justify-center rounded-full border border-white/20 bg-white/5">
            <div className="flex h-28 w-28 items-center justify-center rounded-full bg-white text-black">
              <FiArrowRight size={42} />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

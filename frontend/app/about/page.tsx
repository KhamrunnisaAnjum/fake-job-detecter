import { FiShield, FiGithub, FiCode } from "react-icons/fi";

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-[#F6F7FB] p-10">
      <div className="max-w-5xl mx-auto">
        <p className="uppercase tracking-[4px] text-sm text-neutral-500">
          JobX
        
        </p>

        <h1 className="mt-2 text-5xl font-bold">About</h1>

        <div className="mt-10 rounded-3xl bg-white p-10 shadow-sm">
          <div className="flex items-center gap-5">
            <div className="rounded-full bg-black p-5">
              <FiShield size={40} className="text-white" />
            </div>

            <div>
              <h2 className="text-3xl font-bold">JobX </h2>

              <p className="text-neutral-500">
                AI Powered Fake Job Posting Detector
              </p>
            </div>
          </div>

          <p className="mt-8 text-lg leading-8 text-neutral-600">
            JobX helps users identify fraudulent job advertisements
            using Machine Learning, Natural Language Processing and intelligent
            risk analysis.
          </p>

          <div className="grid grid-cols-2 gap-6 mt-10">
            <div className="rounded-2xl bg-neutral-100 p-6">
              <FiCode size={28} />

              <h3 className="mt-4 text-xl font-bold">Tech Stack</h3>

              <p className="mt-3 text-neutral-600">
                Next.js
                <br />
                React
                <br />
                Tailwind CSS
                <br />
                FastAPI
                <br />
                Scikit-learn
              </p>
            </div>

            <div className="rounded-2xl bg-neutral-100 p-6">
              <FiGithub size={28} />

              <h3 className="mt-4 text-xl font-bold">Version</h3>

              <p className="mt-3 text-neutral-600">
                JobX v1.0
                <br />
                Final Year Project
                <br />
                AI + Machine Learning
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

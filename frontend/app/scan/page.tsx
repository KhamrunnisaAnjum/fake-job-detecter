"use client";

import { useState } from "react";
import {
  FiSearch,
  FiAlertTriangle,
  FiCheckCircle,
  FiLoader,
} from "react-icons/fi";

type ScanResult = {
  risk: "High Risk" | "Medium Risk" | "Low Risk";
  prediction: string;
  probability: number;
};

export default function ScanPage() {
  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
  const [salary, setSalary] = useState("");
  const [requirements, setRequirements] = useState("");
  const [description, setDescription] = useState("");

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState<ScanResult | null>(null);

  async function analyzeJob() {
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title,
          company,
          description,
          requirements,
          salary,
        }),
      });

      const data = await res.json();

      setResult(data);
    } catch (err) {
      alert("Backend not running.");
      console.log(err);
    }

    setLoading(false);
  }

  function getColor() {
    if (!result) return "bg-gray-500";

    if (result.risk === "High Risk") return "bg-red-500";

    if (result.risk === "Medium Risk") return "bg-yellow-500";

    return "bg-green-500";
  }

  function getTextColor() {
    if (!result) return "text-gray-700";

    if (result.risk === "High Risk") return "text-red-600";

    if (result.risk === "Medium Risk") return "text-yellow-600";

    return "text-green-600";
  }

  function getIcon() {
    if (!result) return <FiAlertTriangle size={28} />;

    if (result.risk === "Low Risk") return <FiCheckCircle size={32} />;

    return <FiAlertTriangle size={32} />;
  }

  return (
    <div className="min-h-screen bg-[#F4F7FC] p-10">
      <div className="mx-auto max-w-6xl">
        <h1 className="text-5xl font-bold">JobX AI Scanner</h1>

        <p className="mt-3 text-neutral-500">
          Detect fake job advertisements using Machine Learning.
        </p>

        <div className="mt-10 rounded-3xl bg-white p-8 shadow">
          <label className="font-semibold">Job Title</label>

          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="mt-3 w-full rounded-xl border p-4"
            placeholder="Software Engineer"
          />

          <label className="mt-8 block font-semibold">Company</label>

          <input
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="mt-3 w-full rounded-xl border p-4"
            placeholder="Google"
          />

          <label className="mt-8 block font-semibold">Salary</label>

          <input
            value={salary}
            onChange={(e) => setSalary(e.target.value)}
            className="mt-3 w-full rounded-xl border p-4"
            placeholder="20 LPA"
          />

          <label className="mt-8 block font-semibold">Requirements</label>

          <textarea
            rows={5}
            value={requirements}
            onChange={(e) => setRequirements(e.target.value)}
            className="mt-3 w-full rounded-xl border p-4"
            placeholder="Python, React, Bachelor's Degree..."
          />

          <label className="mt-8 block font-semibold">Job Description</label>

          <textarea
            rows={10}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="mt-3 w-full rounded-xl border p-4"
            placeholder="Paste complete job description..."
          />

          <button
            onClick={analyzeJob}
            disabled={loading}
            className="mt-8 flex items-center gap-3 rounded-xl bg-black px-8 py-4 text-white transition hover:scale-105"
          >
            {loading ? (
              <>
                <FiLoader className="animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <FiSearch />
                Analyze Job
              </>
            )}
          </button>

          {result && (
            <div className="mt-10 rounded-3xl border bg-gray-50 p-8">
              <div className="flex items-center gap-5">
                <div
                  className={`flex h-16 w-16 items-center justify-center rounded-full text-white ${getColor()}`}
                >
                  {getIcon()}
                </div>

                <div>
                  <p className="text-sm text-gray-500">AI Prediction</p>

                  <h2 className={`text-3xl font-bold ${getTextColor()}`}>
                    {result.risk}
                  </h2>

                  <p className="mt-1 text-gray-600">{result.prediction}</p>
                </div>
              </div>

              <div className="mt-8">
                <div className="mb-2 flex justify-between">
                  <span>Fraud Probability</span>

                  <span className="font-bold">{result.probability}%</span>
                </div>

                <div className="h-4 overflow-hidden rounded-full bg-gray-200">
                  <div
                    className={`h-4 transition-all duration-700 ${getColor()}`}
                    style={{
                      width: `${result.probability}%`,
                    }}
                  />
                </div>
              </div>

              <div className="mt-8 rounded-2xl bg-white p-6">
                <h3 className="mb-4 text-xl font-semibold">AI Analysis</h3>

                {result.risk === "High Risk" && (
                  <ul className="space-y-3 text-gray-700">
                    <li>⚠️ High fraud probability detected.</li>
                    <li>⚠️ Verify company website.</li>
                    <li>⚠️ Never pay registration fees.</li>
                    <li>⚠️ Check recruiter email carefully.</li>
                    <li>⚠️ Research company before applying.</li>
                  </ul>
                )}

                {result.risk === "Medium Risk" && (
                  <ul className="space-y-3 text-gray-700">
                    <li>⚠️ Some suspicious indicators detected.</li>
                    <li>⚠️ Verify employer identity.</li>
                    <li>⚠️ Apply only through official websites.</li>
                  </ul>
                )}

                {result.risk === "Low Risk" && (
                  <ul className="space-y-3 text-gray-700">
                    <li>✅ No major fraud indicators detected.</li>
                    <li>✅ Job appears legitimate.</li>
                    <li>✅ Still verify through official company website.</li>
                  </ul>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
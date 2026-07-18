"use client";

import { useState } from "react";
import {
  Search,
  AlertTriangle,
  CheckCircle,
  Loader2,
  ShieldAlert,
  ShieldCheck,
  AlertOctagon,
  Info
} from "lucide-react";

type ScanResult = {
  risk: "High Risk" | "Medium Risk" | "Low Risk";
  prediction: string;
  probability: number;
  warnings: string[];
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
          title: title || "",
          company: company || "",
          description: description || "",
          requirements: requirements || "",
          salary: salary || "",
        }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("Backend not running. Please start FastAPI.");
      console.error(err);
    }

    setLoading(false);
  }

  function getRiskStyles() {
    if (!result) return { bg: "bg-gray-100", border: "border-gray-200", text: "text-gray-700", icon: "text-gray-500", progress: "bg-gray-500" };

    if (result.risk === "High Risk") {
      return { 
        bg: "bg-red-50", 
        border: "border-red-200", 
        text: "text-red-700", 
        icon: "text-red-600",
        progress: "bg-red-600"
      };
    }
    if (result.risk === "Medium Risk") {
      return { 
        bg: "bg-orange-50", 
        border: "border-orange-200", 
        text: "text-orange-700", 
        icon: "text-orange-500",
        progress: "bg-orange-500"
      };
    }
    return { 
      bg: "bg-emerald-50", 
      border: "border-emerald-200", 
      text: "text-emerald-700", 
      icon: "text-emerald-600",
      progress: "bg-emerald-500"
    };
  }

  function getIcon() {
    if (!result) return <Info className="h-10 w-10" />;
    if (result.risk === "High Risk") return <ShieldAlert className="h-12 w-12" />;
    if (result.risk === "Medium Risk") return <AlertTriangle className="h-12 w-12" />;
    return <ShieldCheck className="h-12 w-12" />;
  }

  const riskStyles = getRiskStyles();

  return (
    <div className="max-w-6xl mx-auto pb-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="mb-8">
        <h1 className="text-4xl font-extrabold tracking-tight text-gray-900">Job Scanner</h1>
        <p className="mt-2 text-lg text-gray-500">
          Analyze job postings with our AI-powered detection engine to identify potential scams.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Input Form */}
        <div className="lg:col-span-7 space-y-6">
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 sm:p-8 transition-shadow hover:shadow-md duration-300">
            <h2 className="text-xl font-semibold mb-6 flex items-center">
              <span className="bg-black text-white p-2 rounded-lg mr-3">
                <Search size={18} />
              </span>
              Job Details
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div className="col-span-1 md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Job Title</label>
                <input
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
                  placeholder="e.g. Senior Software Engineer"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Company Name</label>
                <input
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
                  placeholder="e.g. Google"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Salary Offered</label>
                <input
                  value={salary}
                  onChange={(e) => setSalary(e.target.value)}
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
                  placeholder="e.g. $120,000/year"
                />
              </div>

              <div className="col-span-1 md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Requirements</label>
                <textarea
                  rows={3}
                  value={requirements}
                  onChange={(e) => setRequirements(e.target.value)}
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all resize-none"
                  placeholder="Paste job requirements here..."
                />
              </div>

              <div className="col-span-1 md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Full Job Description</label>
                <textarea
                  rows={6}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all resize-none"
                  placeholder="Paste the complete job description here..."
                />
              </div>
            </div>

            <button
              onClick={analyzeJob}
              disabled={loading || (!title && !description)}
              className="mt-8 w-full flex justify-center items-center gap-2 rounded-xl bg-black px-8 py-4 text-white font-medium hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin h-5 w-5" />
                  Running AI Analysis...
                </>
              ) : (
                <>
                  <Search className="h-5 w-5" />
                  Analyze Posting
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-5">
          {result ? (
            <div className={`rounded-2xl border ${riskStyles.border} ${riskStyles.bg} p-6 sm:p-8 shadow-sm transition-all duration-500 animate-in zoom-in-95`}>
              <div className="flex items-center gap-4 mb-6">
                <div className={`${riskStyles.icon}`}>
                  {getIcon()}
                </div>
                <div>
                  <p className="text-sm font-semibold uppercase tracking-wider text-gray-500">Final Assessment</p>
                  <h2 className={`text-3xl font-bold ${riskStyles.text}`}>
                    {result.risk}
                  </h2>
                </div>
              </div>

              <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm mb-6">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600 font-medium text-sm">Fraud Probability</span>
                  <span className={`font-bold ${riskStyles.text}`}>{result.probability}%</span>
                </div>
                <div className="h-3 w-full bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className={`h-full transition-all duration-1000 ease-out ${riskStyles.progress}`}
                    style={{ width: `${result.probability}%` }}
                  />
                </div>
              </div>

              {/* AI Rule Warnings */}
              {result.warnings && result.warnings.length > 0 && (
                <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm mb-6">
                  <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    <AlertOctagon size={18} className="text-orange-500" />
                    Specific Warnings Detected
                  </h3>
                  <ul className="space-y-3">
                    {result.warnings.map((warning, idx) => (
                      <li key={idx} className="text-sm text-gray-700 flex items-start">
                        <span className="mr-2 mt-0.5">•</span>
                        {warning.replace("⚠️", "")}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* General Guidance based on Risk */}
              <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
                <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <ShieldCheck size={18} className="text-blue-500" />
                  Recommendation
                </h3>
                {result.risk === "High Risk" && (
                  <p className="text-sm text-gray-600 leading-relaxed">
                    This job posting exhibits multiple strong indicators of a scam. <strong>Do not provide any personal information, banking details, or upfront payments.</strong> We strongly advise ignoring this listing.
                  </p>
                )}
                {result.risk === "Medium Risk" && (
                  <p className="text-sm text-gray-600 leading-relaxed">
                    There are some suspicious elements in this posting. Proceed with caution. Verify the company's official website and ensure you are communicating through official corporate channels before sharing information.
                  </p>
                )}
                {result.risk === "Low Risk" && (
                  <p className="text-sm text-gray-600 leading-relaxed">
                    This posting appears legitimate and lacks common fraud indicators. However, always remain vigilant and follow standard safety practices when applying for jobs online.
                  </p>
                )}
              </div>
            </div>
          ) : (
            <div className="h-full bg-white rounded-2xl border border-gray-200 border-dashed p-8 flex flex-col items-center justify-center text-center text-gray-500 shadow-sm">
              <Search className="h-12 w-12 text-gray-300 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Waiting for Input</h3>
              <p className="text-sm max-w-xs">
                Fill out the job details on the left and click "Analyze Posting" to see the AI assessment here.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
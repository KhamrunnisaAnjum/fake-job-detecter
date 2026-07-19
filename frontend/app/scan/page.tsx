"use client";
<<<<<<< HEAD

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
=======
import { apiFetch } from "@/utils/api";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
    AlertTriangle, 
    ShieldCheck, 
    Search, 
    FileText, 
    AlignLeft,
    CheckCircle2,
    XCircle,
    Info
} from "lucide-react";

export default function ScanPage() {
    const [activeTab, setActiveTab] = useState<"structured" | "raw">("structured");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);

    // Form states
    const [title, setTitle] = useState("");
    const [company, setCompany] = useState("");
    const [salary, setSalary] = useState("");
    const [requirements, setRequirements] = useState("");
    const [description, setDescription] = useState("");
    const [rawText, setRawText] = useState("");

    const handleScan = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);

        let reqBody = { title, company, salary, requirements, description };

        try {
            const res = await apiFetch("http://127.0.0.1:8000/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(reqBody)
            });
            if (res.ok) {
                const data = await res.json();
                setResult(data);
            }
        } catch (error) {
            console.error("API Error", error);
        } finally {
            setLoading(false);
        }
    };

    const getRiskColor = (risk: string) => {
        if (risk === "High Risk") return "#DC2626"; // Danger
        if (risk === "Medium Risk") return "#F59E0B"; // Warning
        return "#16A34A"; // Success
    };

    return (
        <div className="w-full flex flex-col xl:flex-row gap-6 items-start">
            
            {/* LEFT COLUMN: Input Form */}
            <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="w-full xl:w-[50%] bg-[#FFFFFF] rounded-[18px] shadow-sm border border-[#E5E7EB] overflow-hidden flex flex-col"
            >
                <div className="p-6 border-b border-[#E5E7EB]">
                    <h2 className="text-lg font-semibold text-[#111111] tracking-tight">Scan New Job</h2>
                    <p className="text-sm text-[#6B7280] mt-1">Analyze a job posting using the Hybrid AI Engine.</p>
                </div>

                <form onSubmit={handleScan} className="p-6 flex flex-col gap-5 flex-1 bg-[#FFFFFF]">
                    <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-xs font-semibold text-[#111111] mb-1.5">Job Title</label>
                                <input type="text" required value={title} onChange={e=>setTitle(e.target.value)} className="w-full bg-[#FFFFFF] border border-[#E5E7EB] rounded-lg px-3 py-2.5 text-sm focus:ring-1 focus:ring-[#111111] focus:border-[#111111] transition-all outline-none" placeholder="e.g. Software Engineer" />
                            </div>
                            <div>
                                <label className="block text-xs font-semibold text-[#111111] mb-1.5">Company Name</label>
                                <input type="text" required value={company} onChange={e=>setCompany(e.target.value)} className="w-full bg-[#FFFFFF] border border-[#E5E7EB] rounded-lg px-3 py-2.5 text-sm focus:ring-1 focus:ring-[#111111] focus:border-[#111111] transition-all outline-none" placeholder="e.g. Google" />
                            </div>
                        </div>
                        <div>
                            <label className="block text-xs font-semibold text-[#111111] mb-1.5">Salary Offer</label>
                            <input type="text" required value={salary} onChange={e=>setSalary(e.target.value)} className="w-full bg-[#FFFFFF] border border-[#E5E7EB] rounded-lg px-3 py-2.5 text-sm focus:ring-1 focus:ring-[#111111] focus:border-[#111111] transition-all outline-none" placeholder="e.g. $120,000 / year" />
                        </div>
                        <div>
                            <label className="block text-xs font-semibold text-[#111111] mb-1.5">Requirements</label>
                            <textarea required value={requirements} onChange={e=>setRequirements(e.target.value)} className="w-full bg-[#FFFFFF] border border-[#E5E7EB] rounded-lg px-3 py-2.5 text-sm focus:ring-1 focus:ring-[#111111] focus:border-[#111111] transition-all outline-none min-h-[80px] resize-none" placeholder="List required skills and experience..."></textarea>
                        </div>
                        <div>
                            <label className="block text-xs font-semibold text-[#111111] mb-1.5">Job Description</label>
                            <textarea required value={description} onChange={e=>setDescription(e.target.value)} className="w-full bg-[#FFFFFF] border border-[#E5E7EB] rounded-lg px-3 py-2.5 text-sm focus:ring-1 focus:ring-[#111111] focus:border-[#111111] transition-all outline-none min-h-[120px] resize-none" placeholder="Paste the full job description here..."></textarea>
                        </div>
                    </div>
                    <div className="pt-4 mt-2">
                        <button 
                            type="submit" 
                            disabled={loading}
                            className="w-full flex items-center justify-center gap-2 bg-[#111111] hover:bg-black text-white font-medium py-3 px-4 rounded-lg transition-colors disabled:opacity-50"
                        >
                            {loading ? (
                                <div className="w-4 h-4 border-2 border-[#FFFFFF]/30 border-t-[#FFFFFF] rounded-full animate-spin"></div>
                            ) : (
                                <><Search className="w-4 h-4" /> Analyze Job</>
                            )}
                        </button>
                    </div>
                </form>
            </motion.div>

            {/* RIGHT COLUMN: Results */}
            <div className="w-full xl:w-[50%] flex flex-col gap-6">
                <AnimatePresence mode="wait">
                    {!result && !loading ? (
                        <motion.div 
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="bg-[#FFFFFF] rounded-[18px] p-10 shadow-sm border border-[#E5E7EB] flex flex-col items-center justify-center text-center h-[500px]"
                        >
                            <div className="w-16 h-16 bg-[#F5F5F4] rounded-full flex items-center justify-center mb-4">
                                <Search className="w-6 h-6 text-[#6B7280]" />
                            </div>
                            <h3 className="text-base font-semibold text-[#111111]">Live Analysis Panel</h3>
                            <p className="text-sm text-[#6B7280] max-w-[250px] mt-2">Submit a job description on the left to generate a comprehensive fraud report.</p>
                        </motion.div>
                    ) : null}

                    {loading && (
                        <motion.div 
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="bg-[#FFFFFF] rounded-[18px] p-10 shadow-sm border border-[#E5E7EB] flex flex-col items-center justify-center text-center h-[500px]"
                        >
                            <div className="w-12 h-12 mb-6 relative">
                                <div className="absolute inset-0 border-2 border-[#E5E7EB] rounded-full"></div>
                                <div className="absolute inset-0 border-2 border-[#111111] border-t-transparent rounded-full animate-spin"></div>
                            </div>
                            <h3 className="text-base font-semibold text-[#111111]">Analyzing Target...</h3>
                            <p className="text-sm text-[#6B7280] mt-2">Checking heuristics, TF-IDF vectors, and risk patterns.</p>
                        </motion.div>
                    )}

                    {result && !loading && (
                        <motion.div 
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex flex-col gap-6"
                        >
                            {/* Score Card */}
                            <div className="bg-[#FFFFFF] rounded-[18px] p-8 shadow-sm border border-[#E5E7EB] flex flex-col items-center relative overflow-hidden">
                                
                                <div className="absolute top-0 left-0 w-full h-1" style={{ backgroundColor: getRiskColor(result.risk) }}></div>
                                
                                <h2 className="text-sm font-semibold text-[#111111] mb-6">AI Fraud Score</h2>
                                
                                {/* Circular Progress */}
                                <div className="relative w-36 h-36 flex items-center justify-center mb-6">
                                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                                        <circle cx="50" cy="50" r="45" fill="none" stroke="#F5F5F4" strokeWidth="6" />
                                        <motion.circle 
                                            initial={{ strokeDasharray: "0 282.7" }}
                                            animate={{ strokeDasharray: `${(result.probability / 100) * 282.7} 282.7` }}
                                            transition={{ duration: 1.2, ease: "easeOut" }}
                                            cx="50" cy="50" r="45" 
                                            fill="none" 
                                            stroke={getRiskColor(result.risk)}
                                            strokeWidth="6" 
                                            strokeLinecap="round"
                                        />
                                    </svg>
                                    <div className="absolute flex flex-col items-center">
                                        <span className="text-3xl font-bold text-[#111111]">{result.probability.toFixed(0)}%</span>
                                    </div>
                                </div>

                                <div className="px-3 py-1 rounded border text-xs font-semibold flex items-center gap-1.5"
                                     style={{ 
                                         backgroundColor: `${getRiskColor(result.risk)}10`, 
                                         color: getRiskColor(result.risk),
                                         borderColor: `${getRiskColor(result.risk)}30`
                                     }}>
                                    {result.risk === 'High Risk' ? <XCircle className="w-3.5 h-3.5"/> : result.risk === 'Medium Risk' ? <AlertTriangle className="w-3.5 h-3.5" /> : <CheckCircle2 className="w-3.5 h-3.5"/>}
                                    {result.prediction}
                                </div>
                            </div>

                            {/* Details Card */}
                            <div className="bg-[#FFFFFF] rounded-[18px] p-8 shadow-sm border border-[#E5E7EB] flex flex-col gap-6">
                                
                                {/* Explanation */}
                                <div>
                                    <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-2">AI Explanation</h3>
                                    <p className="text-sm text-[#111111] leading-relaxed bg-[#F5F5F4] p-4 rounded-lg border border-[#E5E7EB]">
                                        {result.explanation}
                                    </p>
                                </div>

                                {/* Warning Flags */}
                                {result.warning_flags && result.warning_flags.length > 0 && (
                                    <div>
                                        <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-3">Detected Red Flags</h3>
                                        <div className="space-y-2">
                                            {result.warning_flags.map((flag: string, i: number) => (
                                                <div key={i} className="flex items-start gap-2 bg-[#DC2626]/5 p-3 rounded-md border border-[#DC2626]/20">
                                                    <AlertTriangle className="w-4 h-4 text-[#DC2626] shrink-0 mt-0.5" />
                                                    <span className="text-xs font-medium text-[#DC2626] leading-tight">{flag.replace("⚠️", "")}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Recommendation */}
                                <div>
                                    <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-2">Recommended Action</h3>
                                    <div className="p-4 rounded-md border text-sm flex items-center gap-3"
                                         style={{ 
                                            backgroundColor: `${getRiskColor(result.risk)}05`, 
                                            color: getRiskColor(result.risk),
                                            borderColor: `${getRiskColor(result.risk)}30`
                                         }}>
                                        <Info className="w-4 h-4 shrink-0" />
                                        <span className="font-medium">{result.recommended_action}</span>
                                    </div>
                                </div>

                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6
}
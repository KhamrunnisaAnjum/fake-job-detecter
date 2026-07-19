"use client";
<<<<<<< HEAD

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
=======
import { apiFetch } from "@/utils/api";

import { useState } from "react";
import {
  MessageSquareWarning,
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  Loader2,
  AlertOctagon,
  Copy
} from "lucide-react";

type ScanResult = {
  risk: "High Risk" | "Medium Risk" | "Low Risk";
  prediction: string;
  probability: number;
  warnings: string[];
};

export default function AnalyzerPage() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ScanResult | null>(null);

  async function analyzeMessage() {
    setLoading(true);
    setResult(null);

    try {
      const res = await apiFetch("http://127.0.0.1:8000/analyze-message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message || "",
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
    if (!result) return { bg: "bg-gray-100", border: "border-gray-200", text: "text-gray-700", progress: "bg-gray-500" };
    if (result.risk === "High Risk") return { bg: "bg-red-50", border: "border-red-200", text: "text-red-700", progress: "bg-red-600" };
    if (result.risk === "Medium Risk") return { bg: "bg-orange-50", border: "border-orange-200", text: "text-orange-700", progress: "bg-orange-500" };
    return { bg: "bg-emerald-50", border: "border-emerald-200", text: "text-emerald-700", progress: "bg-emerald-500" };
  }

  function getIcon() {
    if (!result) return null;
    if (result.risk === "High Risk") return <ShieldAlert className="h-10 w-10 text-red-600" />;
    if (result.risk === "Medium Risk") return <AlertTriangle className="h-10 w-10 text-orange-500" />;
    return <ShieldCheck className="h-10 w-10 text-emerald-600" />;
  }

  const riskStyles = getRiskStyles();

  return (
    <div className="max-w-4xl mx-auto pb-12 animate-in fade-in duration-500">
      <div className="mb-8 text-center">
        <div className="inline-flex items-center justify-center p-3 bg-gray-100 rounded-full mb-4">
            <MessageSquareWarning size={32} className="text-gray-800" />
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight text-gray-900">Message Analyzer</h1>
        <p className="mt-3 text-lg text-gray-500 max-w-2xl mx-auto">
          Paste suspicious WhatsApp, Telegram, or SMS messages to instantly detect scams, phishing attempts, and fraudulent job offers.
        </p>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 sm:p-8 mb-8">
        <div className="mb-4 flex justify-between items-end">
            <label className="block text-sm font-medium text-gray-700">Paste Message Content</label>
            <button 
                onClick={() => navigator.clipboard.readText().then(text => setMessage(text))}
                className="text-xs flex items-center text-gray-500 hover:text-black transition-colors"
            >
                <Copy size={14} className="mr-1" /> Paste from Clipboard
            </button>
        </div>
        
        <textarea
            rows={8}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="w-full rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all resize-none text-gray-800 leading-relaxed"
            placeholder="E.g., Hi! We are urgently hiring for a part-time role. Work 1 hour a day and earn $500. Click here to chat on Telegram: t.me/fake_recruiter or pay $50 registration fee via UPI..."
        />
        
        <button
            onClick={analyzeMessage}
            disabled={loading || !message.trim()}
            className="mt-6 w-full flex justify-center items-center gap-2 rounded-xl bg-black px-8 py-4 text-white font-medium hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
        >
            {loading ? (
            <>
                <Loader2 className="animate-spin h-5 w-5" />
                Analyzing Message...
            </>
            ) : (
            <>
                <MessageSquareWarning className="h-5 w-5" />
                Scan for Threats
            </>
            )}
        </button>
      </div>

      {result && (
        <div className={`rounded-2xl border ${riskStyles.border} ${riskStyles.bg} p-6 sm:p-8 shadow-sm transition-all duration-500 animate-in slide-in-from-bottom-4`}>
            <div className="flex flex-col md:flex-row gap-8 items-start">
                <div className="flex-1 w-full">
                    <div className="flex items-center gap-4 mb-6">
                        {getIcon()}
                        <div>
                        <p className="text-sm font-semibold uppercase tracking-wider text-gray-500">Analysis Result</p>
                        <h2 className={`text-3xl font-bold ${riskStyles.text}`}>
                            {result.risk}
                        </h2>
                        </div>
                    </div>
                    
                    <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm mb-6">
                        <div className="flex justify-between items-center mb-2">
                        <span className="text-gray-600 font-medium text-sm">Threat Probability</span>
                        <span className={`font-bold ${riskStyles.text}`}>{result.probability}%</span>
                        </div>
                        <div className="h-3 w-full bg-gray-100 rounded-full overflow-hidden">
                        <div
                            className={`h-full transition-all duration-1000 ease-out ${riskStyles.progress}`}
                            style={{ width: `${result.probability}%` }}
                        />
                        </div>
                    </div>
                </div>

                {/* AI Rule Warnings */}
                <div className="flex-1 w-full">
                    <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm h-full">
                        <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                            <AlertOctagon size={18} className={result.warnings.length > 0 ? "text-orange-500" : "text-gray-400"} />
                            Detected Flags
                        </h3>
                        {result.warnings && result.warnings.length > 0 ? (
                            <ul className="space-y-4">
                                {result.warnings.map((warning, idx) => (
                                <li key={idx} className="text-sm text-gray-700 flex items-start bg-orange-50/50 p-3 rounded-lg border border-orange-100">
                                    <span className="mr-2 text-orange-500 mt-0.5">•</span>
                                    {warning.replace("⚠️", "")}
                                </li>
                                ))}
                            </ul>
                        ) : (
                            <div className="text-sm text-gray-500 flex flex-col items-center justify-center h-32 text-center">
                                <ShieldCheck size={32} className="text-emerald-400 mb-2" />
                                No specific scam patterns or links detected by the rule engine.
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
      )}
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6
    </div>
  );
}

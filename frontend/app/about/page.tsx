<<<<<<< HEAD
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
=======
"use client";

import { motion } from "framer-motion";
import { 
    Cpu, 
    Lock, 
    Zap, 
    Database, 
    Server, 
    Code,
    Shield
} from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export default function AboutPage() {
    return (
        <div className="w-full flex flex-col gap-12 pb-12">
            
            {/* Hero Section */}
            <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-[#111111] rounded-[24px] p-12 overflow-hidden relative flex flex-col items-center text-center shadow-lg"
            >
                <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-white rounded-full blur-[120px]"></div>
                </div>
                
                <div className="w-16 h-16 bg-[#FFFFFF]/10 border border-[#FFFFFF]/20 rounded-2xl flex items-center justify-center mb-6 relative z-10 backdrop-blur-md">
                    <Shield className="w-8 h-8 text-white" />
                </div>
                <h1 className="text-4xl md:text-5xl font-bold text-white tracking-tight relative z-10 max-w-2xl leading-tight">
                    Next-Generation Threat Intelligence
                </h1>
                <p className="text-[#A1A1AA] text-lg mt-6 max-w-xl relative z-10">
                    JOBX leverages advanced heuristics and TF-IDF vectorization to identify and neutralize employment fraud before it compromises your data.
                </p>
                <div className="mt-10 flex gap-4 relative z-10">
                    <Link href="/docs">
                        <button 
                            className="bg-white text-black font-semibold py-3 px-6 rounded-lg text-sm hover:bg-gray-100 transition-colors"
                        >
                            View Documentation
                        </button>
                    </Link>
                    <button 
                        onClick={() => alert("Thank you for your interest! Our sales team will reach out to the admin email shortly.")}
                        className="bg-transparent border border-[#FFFFFF]/20 text-white font-semibold py-3 px-6 rounded-lg text-sm hover:bg-[#FFFFFF]/5 transition-colors"
                    >
                        Contact Sales
                    </button>
                </div>
            </motion.div>

            {/* Platform Features Grid */}
            <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="grid grid-cols-1 md:grid-cols-3 gap-6"
            >
                <div className="bg-[#FFFFFF] rounded-[18px] p-8 shadow-sm border border-[#E5E7EB] flex flex-col gap-4">
                    <div className="w-10 h-10 bg-[#F5F5F4] rounded-lg flex items-center justify-center">
                        <Zap className="w-5 h-5 text-[#111111]" />
                    </div>
                    <h3 className="text-base font-semibold text-[#111111]">Real-time Analysis</h3>
                    <p className="text-sm text-[#6B7280] leading-relaxed">
                        Sub-millisecond inference speeds powered by an optimized rule engine and scikit-learn classifier pipelines.
                    </p>
                </div>
                <div className="bg-[#FFFFFF] rounded-[18px] p-8 shadow-sm border border-[#E5E7EB] flex flex-col gap-4">
                    <div className="w-10 h-10 bg-[#F5F5F4] rounded-lg flex items-center justify-center">
                        <Lock className="w-5 h-5 text-[#111111]" />
                    </div>
                    <h3 className="text-base font-semibold text-[#111111]">Privacy First</h3>
                    <p className="text-sm text-[#6B7280] leading-relaxed">
                        Zero-retention policies available. Your data is processed securely and encrypted at rest within our local SQLite instances.
                    </p>
                </div>
                <div className="bg-[#FFFFFF] rounded-[18px] p-8 shadow-sm border border-[#E5E7EB] flex flex-col gap-4">
                    <div className="w-10 h-10 bg-[#F5F5F4] rounded-lg flex items-center justify-center">
                        <Cpu className="w-5 h-5 text-[#111111]" />
                    </div>
                    <h3 className="text-base font-semibold text-[#111111]">Hybrid Architecture</h3>
                    <p className="text-sm text-[#6B7280] leading-relaxed">
                        Combining deterministic heuristic matching with probabilistic machine learning for maximum precision and recall.
                    </p>
                </div>
            </motion.div>

            {/* Tech Stack */}
            <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-[#FFFFFF] rounded-[24px] p-10 md:p-14 shadow-sm border border-[#E5E7EB] flex flex-col md:flex-row gap-12 items-center"
            >
                <div className="flex-1 space-y-6">
                    <h2 className="text-2xl font-bold text-[#111111] tracking-tight">Built on modern foundations.</h2>
                    <p className="text-[#6B7280] text-sm leading-relaxed">
                        JOBX is engineered using industry-standard tools to guarantee reliability, performance, and scalability across all threat vectors.
                    </p>
                    <div className="space-y-4 pt-2">
                        <div className="flex items-center gap-3">
                            <Server className="w-5 h-5 text-[#111111]" />
                            <span className="text-sm font-medium text-[#111111]">FastAPI & Python 3</span>
                        </div>
                        <div className="flex items-center gap-3">
                            <Database className="w-5 h-5 text-[#111111]" />
                            <span className="text-sm font-medium text-[#111111]">SQLite & SQLAlchemy</span>
                        </div>
                        <div className="flex items-center gap-3">
                            <Code className="w-5 h-5 text-[#111111]" />
                            <span className="text-sm font-medium text-[#111111]">Next.js 16 & React</span>
                        </div>
                    </div>
                </div>
                <div className="flex-1 bg-[#F5F5F4] rounded-2xl p-8 border border-[#E5E7EB] w-full flex items-center justify-center min-h-[300px]">
                     <div className="font-mono text-xs text-[#6B7280] space-y-2 opacity-70">
                         <p>{">"} initializing JOBX runtime...</p>
                         <p>{">"} loading tf-idf vectorizer...</p>
                         <p>{">"} loading heuristic engine...</p>
                         <p>{">"} model loaded in 0.04s.</p>
                         <p className="text-[#16A34A]">{"\u2714"} system ready.</p>
                     </div>
                </div>
            </motion.div>

        </div>
    );
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6
}

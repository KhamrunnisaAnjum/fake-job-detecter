"use client";

import { motion } from "framer-motion";
import { ArrowLeft, BookOpen, Shield, Cpu, Lock, Database } from "lucide-react";
import Link from "next/link";

export default function DocsPage() {
    return (
        <div className="w-full max-w-4xl mx-auto flex flex-col gap-10 pb-16">
            
            {/* Header */}
            <div>
                <Link href="/about" className="inline-flex items-center gap-2 text-sm text-[#6B7280] hover:text-[#111111] mb-6 transition-colors">
                    <ArrowLeft className="w-4 h-4" /> Back to About
                </Link>
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-[#111111] rounded-xl flex items-center justify-center shadow-sm">
                        <BookOpen className="w-5 h-5 text-white" />
                    </div>
                    <h1 className="text-3xl font-bold text-[#111111] tracking-tight">JOBX Documentation</h1>
                </div>
                <p className="text-sm text-[#6B7280] mt-3">Comprehensive guide to the JOBX Threat Intelligence Engine v2.0.</p>
            </div>

            {/* Content Sections */}
            <div className="flex flex-col gap-8">
                
                <DocSection title="What is JOBX?" icon={Shield}>
                    JOBX is an advanced employment fraud detection engine designed to protect job seekers and organizations from malicious actors, identity theft schemes, and fake recruitment campaigns. By analyzing textual patterns, metadata, and behavioral flags, it accurately predicts the likelihood of a job posting or recruitment message being fraudulent.
                </DocSection>

                <DocSection title="Core Features" icon={Shield}>
                    <ul className="list-disc pl-5 space-y-2 text-[#374151]">
                        <li><strong>Real-time Inference:</strong> Millisecond latency for processing and scoring text.</li>
                        <li><strong>Hybrid Analysis:</strong> Combines deterministic rules with probabilistic ML.</li>
                        <li><strong>Actionable Insights:</strong> Provides explainable AI indicators for why a scan was flagged.</li>
                        <li><strong>Comprehensive Reporting:</strong> Generates executive-ready PDF analytics and CSV exports.</li>
                    </ul>
                </DocSection>

                <DocSection title="How Detection Works (The ML Model & Heuristic Engine)" icon={Cpu}>
                    <p className="mb-4">The core pipeline consists of two distinct layers working in tandem:</p>
                    <ol className="list-decimal pl-5 space-y-4 text-[#374151]">
                        <li>
                            <strong>The Heuristic Engine:</strong> Scans for deterministic patterns such as requests for upfront payment, unverified domains, excessive urgency, and requests for sensitive personal information (SSN, Bank Details). This layer acts as a strict firewall.
                        </li>
                        <li>
                            <strong>The Machine Learning Model:</strong> A scikit-learn pipeline utilizing <code>TF-IDF Vectorization</code> coupled with a <code>RandomForestClassifier</code>. It has been trained on tens of thousands of verified real and fake job postings. It catches nuanced linguistic patterns that rule-based engines miss.
                        </li>
                    </ol>
                </DocSection>

                <DocSection title="Risk Levels" icon={Shield}>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2">
                        <div className="p-4 bg-[#FEF2F2] border border-[#FECACA] rounded-xl">
                            <h4 className="font-semibold text-[#DC2626]">High Risk (80-100%)</h4>
                            <p className="text-xs text-[#991B1B] mt-1">Severe indicators of fraud. Do not engage or share personal data.</p>
                        </div>
                        <div className="p-4 bg-[#FFFBEB] border border-[#FDE68A] rounded-xl">
                            <h4 className="font-semibold text-[#D97706]">Medium Risk (40-79%)</h4>
                            <p className="text-xs text-[#92400E] mt-1">Suspicious patterns detected. Proceed with extreme caution and verify the source.</p>
                        </div>
                        <div className="p-4 bg-[#F0FDF4] border border-[#BBF7D0] rounded-xl">
                            <h4 className="font-semibold text-[#16A34A]">Low Risk (0-39%)</h4>
                            <p className="text-xs text-[#166534] mt-1">Appears legitimate based on known patterns. Standard diligence applies.</p>
                        </div>
                    </div>
                </DocSection>

                <DocSection title="Privacy & Security" icon={Lock}>
                    Your privacy is paramount. Scans are processed entirely in memory or encrypted at rest within our local SQLite databases. We enforce strict zero-retention policies on sensitive personally identifiable information (PII). Only you can view your private scan history.
                </DocSection>

                <DocSection title="Technologies Used" icon={Database}>
                    <ul className="list-none space-y-2 text-[#374151]">
                        <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-[#111111]"></span> <strong>Frontend:</strong> Next.js 16 (React), TailwindCSS, Framer Motion, Recharts</li>
                        <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-[#111111]"></span> <strong>Backend:</strong> FastAPI, Python 3.10+, Uvicorn</li>
                        <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-[#111111]"></span> <strong>Database:</strong> SQLite with SQLAlchemy ORM</li>
                        <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-[#111111]"></span> <strong>Machine Learning:</strong> scikit-learn, joblib, nltk</li>
                        <li className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-[#111111]"></span> <strong>PDF Generation:</strong> fpdf2, matplotlib</li>
                    </ul>
                </DocSection>

                <div className="mt-8 pt-8 border-t border-[#E5E7EB] flex justify-between items-center text-sm text-[#6B7280]">
                    <span>Version: 2.0.0-stable</span>
                    <span>Developer: Internal Security Team</span>
                </div>
            </div>

        </div>
    );
}

function DocSection({ title, icon: Icon, children }: any) {
    return (
        <motion.div 
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="bg-[#FFFFFF] border border-[#E5E7EB] rounded-2xl p-8 shadow-sm"
        >
            <h2 className="text-xl font-bold text-[#111111] mb-4 flex items-center gap-3">
                <Icon className="w-5 h-5 text-[#6B7280]" />
                {title}
            </h2>
            <div className="text-sm text-[#4B5563] leading-relaxed">
                {children}
            </div>
        </motion.div>
    );
}

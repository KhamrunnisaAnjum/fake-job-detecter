"use client";

import { CheckCircle2, ShieldCheck, Cpu, Database, Layout } from "lucide-react";

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto pb-12 animate-in fade-in duration-500">
      <div className="mb-12 text-center">
        <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 mb-4">About JobX<span className="text-gray-400">.ai</span></h1>
        <p className="text-xl text-gray-500 max-w-2xl mx-auto">
          An advanced AI-powered security platform designed to detect and prevent employment fraud.
        </p>
      </div>

      <div className="space-y-12">
        {/* Objective */}
        <section className="bg-white rounded-3xl p-8 sm:p-10 border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 mb-6">
             <ShieldCheck className="h-8 w-8 text-black" />
             <h2 className="text-2xl font-bold text-gray-900">Project Objective</h2>
          </div>
          <p className="text-gray-600 leading-relaxed text-lg">
            JobX was developed as a comprehensive engineering project to tackle the rising threat of online employment scams. By combining state-of-the-art Machine Learning models with an intelligent heuristic rule engine, JobX analyzes job postings and recruiter communications in real-time. Our goal is to provide a reliable safety net for job seekers, ensuring they can navigate the job market without falling victim to phishing, advance-fee fraud, or identity theft.
          </p>
        </section>

        {/* Features Grid */}
        <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-6 px-2">Core Features</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <FeatureCard 
                    title="Real-time ML Inference" 
                    desc="Pre-trained Scikit-learn models evaluate job descriptions using TF-IDF vectorization to predict fraud probability instantly."
                />
                <FeatureCard 
                    title="Intelligent Rule Engine" 
                    desc="Scans for suspicious patterns including Telegram links, crypto requests, urgency language, and unrealistic salaries."
                />
                <FeatureCard 
                    title="Message Analyzer" 
                    desc="Dedicated tool to analyze WhatsApp and Telegram messages from unsolicited recruiters for common scam indicators."
                />
                <FeatureCard 
                    title="Advanced Analytics" 
                    desc="Comprehensive dashboard with visual reports detailing risk distribution, scan history trends, and latest detected threats."
                />
            </div>
        </section>

        {/* Tech Stack */}
        <section className="bg-black text-white rounded-3xl p-8 sm:p-10 shadow-lg">
          <h2 className="text-2xl font-bold mb-8">Technology Stack</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
             <div className="space-y-4">
                 <div className="flex items-center gap-2 text-gray-300">
                     <Layout size={20} /> <span className="font-semibold text-white">Frontend</span>
                 </div>
                 <ul className="space-y-2 text-sm text-gray-400">
                     <li>• Next.js 16 (App Router)</li>
                     <li>• React & TypeScript</li>
                     <li>• Tailwind CSS (v4)</li>
                     <li>• Recharts & Lucide Icons</li>
                 </ul>
             </div>
             <div className="space-y-4">
                 <div className="flex items-center gap-2 text-gray-300">
                     <Cpu size={20} /> <span className="font-semibold text-white">Backend & AI</span>
                 </div>
                 <ul className="space-y-2 text-sm text-gray-400">
                     <li>• Python FastAPI</li>
                     <li>• Scikit-learn (Logistic Regression)</li>
                     <li>• Custom NLP Rule Engine</li>
                     <li>• Joblib Model Serialization</li>
                 </ul>
             </div>
             <div className="space-y-4">
                 <div className="flex items-center gap-2 text-gray-300">
                     <Database size={20} /> <span className="font-semibold text-white">Database</span>
                 </div>
                 <ul className="space-y-2 text-sm text-gray-400">
                     <li>• SQLite Relational Database</li>
                     <li>• SQLAlchemy ORM</li>
                     <li>• Pydantic Data Validation</li>
                 </ul>
             </div>
          </div>
        </section>

        {/* Future Scope & Credits */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <section className="bg-white rounded-3xl p-8 border border-gray-200 shadow-sm">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Future Scope</h2>
                <ul className="space-y-3">
                    <li className="flex items-start gap-2 text-gray-600 text-sm">
                        <CheckCircle2 size={16} className="text-emerald-500 shrink-0 mt-0.5" />
                        Integration with Deep Learning models (BERT/RoBERTa) for improved context understanding.
                    </li>
                    <li className="flex items-start gap-2 text-gray-600 text-sm">
                        <CheckCircle2 size={16} className="text-emerald-500 shrink-0 mt-0.5" />
                        Chrome Extension to automatically scan job boards like LinkedIn and Indeed.
                    </li>
                    <li className="flex items-start gap-2 text-gray-600 text-sm">
                        <CheckCircle2 size={16} className="text-emerald-500 shrink-0 mt-0.5" />
                        Crowdsourced reporting system to update the rule engine dynamically.
                    </li>
                </ul>
            </section>
            
            <section className="bg-white rounded-3xl p-8 border border-gray-200 shadow-sm flex flex-col justify-center">
                <h2 className="text-xl font-bold text-gray-900 mb-2">Developer Credits</h2>
                <p className="text-gray-500 text-sm mb-6">Designed and developed as a final-year engineering project.</p>
                <div className="flex items-center gap-4">
                    <div className="h-12 w-12 rounded-full bg-gray-100 flex items-center justify-center text-lg font-bold text-gray-700">
                        SD
                    </div>
                    <div>
                        <p className="font-medium text-gray-900">Student Developer</p>
                        <p className="text-sm text-gray-500">Lead Full Stack & AI Engineer</p>
                    </div>
                </div>
            </section>
        </div>
      </div>
    </div>
  );
}

function FeatureCard({ title, desc }: { title: string, desc: string }) {
    return (
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
            <h3 className="font-semibold text-gray-900 mb-2 text-lg">{title}</h3>
            <p className="text-sm text-gray-500 leading-relaxed">{desc}</p>
        </div>
    )
}

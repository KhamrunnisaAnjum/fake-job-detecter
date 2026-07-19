"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { ShieldCheck, Cpu, Search, Brain, ArrowLeft, Eye, EyeOff } from "lucide-react";
import Link from "next/link";

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showFeatures, setShowFeatures] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // Validation
    if (!name.trim()) {
        setError("Full Name cannot be empty.");
        return;
    }
    if (password.length < 8) {
        setError("Password must be at least 8 characters.");
        return;
    }
    if (password !== confirmPassword) {
        setError("Passwords do not match.");
        return;
    }

    setLoading(true);
    
    try {
        const res = await fetch("http://localhost:8000/api/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password })
        });
        
        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.detail || "Email already exists or registration failed.");
        }
        
        // Success redirect
        router.push("/login?registered=true");
    } catch (err: any) {
        setError(err.message);
        setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen w-full items-center justify-center bg-[#F5F5F4] text-[#111111] p-4 font-sans relative">
      
      {/* Main Container */}
      <div className="w-full max-w-[1000px] h-[650px] bg-white rounded-[24px] shadow-sm border border-[#E5E7EB] flex overflow-hidden">
        
        {/* Left Column: Register Form */}
        <div className="w-full lg:w-1/2 flex flex-col p-10 lg:p-14 relative bg-white">
          <div className="flex-1 flex flex-col justify-center max-w-[320px] mx-auto w-full">
              <h1 className="text-3xl font-bold text-[#111111] mb-2 tracking-tight">Create Account</h1>
              <p className="text-[#6B7280] text-sm font-medium mb-8">Join JOBX to secure your career</p>

              {error && (
                  <div className="mb-6 p-3 bg-[#DC2626]/10 text-[#DC2626] text-sm font-medium rounded-xl text-center border border-[#DC2626]/20">
                      {error}
                  </div>
              )}

              <form onSubmit={handleRegister} className="space-y-4">
                  <div>
                      <input 
                          type="text" 
                          value={name}
                          onChange={(e) => setName(e.target.value)}
                          placeholder="Full Name" 
                          className="w-full bg-[#F5F5F4] border border-[#E5E7EB] text-[#111111] placeholder-[#6B7280] rounded-xl px-4 py-3 focus:outline-none focus:ring-1 focus:ring-[#DC2626] focus:border-[#DC2626] transition-all text-sm font-medium"
                          required
                      />
                  </div>
                  <div>
                      <input 
                          type="email" 
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          placeholder="Email Address" 
                          className="w-full bg-[#F5F5F4] border border-[#E5E7EB] text-[#111111] placeholder-[#6B7280] rounded-xl px-4 py-3 focus:outline-none focus:ring-1 focus:ring-[#DC2626] focus:border-[#DC2626] transition-all text-sm font-medium"
                          required
                      />
                  </div>
                  <div className="relative">
                      <input 
                          type={showPassword ? "text" : "password"}
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                          placeholder="Password (8+ characters)" 
                          className="w-full bg-[#F5F5F4] border border-[#E5E7EB] text-[#111111] placeholder-[#6B7280] rounded-xl px-4 py-3 focus:outline-none focus:ring-1 focus:ring-[#DC2626] focus:border-[#DC2626] transition-all text-sm font-medium pr-10"
                          required
                      />
                      <button 
                          type="button" 
                          onClick={() => setShowPassword(!showPassword)} 
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-[#6B7280] hover:text-[#111111] transition-colors"
                      >
                          {showPassword ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                      </button>
                  </div>
                  <div className="relative">
                      <input 
                          type={showConfirmPassword ? "text" : "password"}
                          value={confirmPassword}
                          onChange={(e) => setConfirmPassword(e.target.value)}
                          placeholder="Confirm Password" 
                          className="w-full bg-[#F5F5F4] border border-[#E5E7EB] text-[#111111] placeholder-[#6B7280] rounded-xl px-4 py-3 focus:outline-none focus:ring-1 focus:ring-[#DC2626] focus:border-[#DC2626] transition-all text-sm font-medium pr-10"
                          required
                      />
                      <button 
                          type="button" 
                          onClick={() => setShowConfirmPassword(!showConfirmPassword)} 
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-[#6B7280] hover:text-[#111111] transition-colors"
                      >
                          {showConfirmPassword ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                      </button>
                  </div>

                  <button 
                      type="submit" 
                      disabled={loading}
                      className="w-full bg-[#DC2626] hover:bg-[#B91C1C] text-white font-bold py-3 px-4 rounded-xl mt-4 transition-colors duration-200 text-sm disabled:opacity-50"
                  >
                      {loading ? "Creating Account..." : "Create Account"}
                  </button>

                  <div className="text-center mt-6">
                      <Link href="/login" className="text-sm font-semibold text-[#111111] hover:underline">
                          Already have an account? Login
                      </Link>
                  </div>
              </form>
          </div>
        </div>

        {/* Right Column: Image or Features */}
        <div className="hidden lg:block w-1/2 relative bg-[#111111] overflow-hidden">
            <AnimatePresence mode="wait">
                {!showFeatures ? (
                    <motion.div 
                        key="image-panel"
                        initial={{ opacity: 0, x: 50 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 50 }}
                        transition={{ duration: 0.5 }}
                        className="absolute inset-0 bg-cover bg-center"
                        style={{ backgroundImage: "url('/login-bg.png')" }}
                    >
                        <div className="absolute inset-0 bg-black/20"></div>
                        
                        {/* Top header on image */}
                        <div className="absolute top-8 right-8 flex justify-between text-white font-medium text-sm z-10">
                            <span>JOBX</span>
                        </div>

                        {/* Flip Button */}
                        <div className="absolute bottom-10 left-10 z-10">
                            <button 
                                onClick={() => setShowFeatures(true)} 
                                className="w-12 h-12 rounded-full bg-white/10 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-white/20 transition-all group"
                            >
                                <ArrowLeft className="w-6 h-6 group-hover:-translate-x-1 transition-transform" />
                            </button>
                        </div>
                    </motion.div>
                ) : (
                    <motion.div
                        key="features-panel"
                        initial={{ opacity: 0, x: -50 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -50 }}
                        transition={{ duration: 0.5 }}
                        className="absolute inset-0 bg-[#000000] flex flex-col justify-center p-12"
                    >
                        <div className="relative z-10 space-y-8">
                            {/* Info Block 1 */}
                            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="flex items-center gap-6 group cursor-pointer">
                                <div className="w-14 h-14 rounded-[14px] bg-[#111111] border border-[#222] flex items-center justify-center shrink-0 group-hover:bg-[#222] transition-colors">
                                    <Cpu className="w-6 h-6 text-white" />
                                </div>
                                <div className="flex-1">
                                    <h3 className="font-bold text-white text-[15px] mb-1">Heuristic Engine</h3>
                                    <p className="text-[#6B7280] text-xs">Rule-based pattern matching for phishing.</p>
                                </div>
                            </motion.div>

                            {/* Info Block 2 */}
                            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="flex items-center gap-6 group cursor-pointer">
                                <div className="w-14 h-14 rounded-[14px] bg-[#111111] border border-[#222] flex items-center justify-center shrink-0 group-hover:bg-[#222] transition-colors">
                                    <Search className="w-6 h-6 text-white" />
                                </div>
                                <div className="flex-1">
                                    <h3 className="font-bold text-white text-[15px] mb-1">Message Analyzer</h3>
                                    <p className="text-[#6B7280] text-xs">Scan WhatsApp and Telegram messages instantly.</p>
                                </div>
                            </motion.div>

                            {/* Info Block 3 */}
                            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="flex items-center gap-6 group cursor-pointer">
                                <div className="w-14 h-14 rounded-[14px] bg-[#111111] border border-[#222] flex items-center justify-center shrink-0 group-hover:bg-[#222] transition-colors">
                                    <Brain className="w-6 h-6 text-white" />
                                </div>
                                <div className="flex-1">
                                    <h3 className="font-bold text-white text-[15px] mb-1">Logistic Regression</h3>
                                    <p className="text-[#6B7280] text-xs">TF-IDF vectorization via Scikit-Learn models.</p>
                                </div>
                            </motion.div>

                            {/* Info Block 4 */}
                            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="flex items-center gap-6 group cursor-pointer">
                                <div className="w-14 h-14 rounded-[14px] bg-[#111111] border border-[#222] flex items-center justify-center shrink-0 group-hover:bg-[#222] transition-colors">
                                    <ShieldCheck className="w-6 h-6 text-white" />
                                </div>
                                <div className="flex-1">
                                    <h3 className="font-bold text-white text-[15px] mb-1">Advanced Threat Detection</h3>
                                    <p className="text-[#6B7280] text-xs">Protect yourself against employment fraud.</p>
                                </div>
                            </motion.div>
                        </div>
                        
                        {/* Flip Back Button */}
                        <div className="absolute top-8 right-8">
                            <button 
                                onClick={() => setShowFeatures(false)} 
                                className="w-10 h-10 rounded-full border border-[#222] flex items-center justify-center text-white hover:bg-[#222] transition-all group"
                            >
                                <ArrowLeft className="w-5 h-5 group-hover:translate-x-1 transition-transform rotate-180" />
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>

      </div>
    </div>
  );
}

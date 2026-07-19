"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { ShieldCheck, Cpu, Search, Brain, ArrowRight, Eye, EyeOff } from "lucide-react";
import Link from "next/link";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState("");
  const [showFeatures, setShowFeatures] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showResetModal, setShowResetModal] = useState(false);
  const [resetEmail, setResetEmail] = useState("");

  useEffect(() => {
    if (searchParams.get("registered") === "true") {
      setToast("Account created successfully. Please login.");
    }
  }, [searchParams]);

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    
    try {
        const res = await fetch("http://localhost:8000/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        
        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.detail || "Incorrect Email or Password.");
        }
        
        const data = await res.json();
        document.cookie = `jobx_token=${data.token}; path=/; max-age=604800; samesite=strict`;
        
        router.push("/dashboard");
    } catch (err: any) {
        setError(err.message);
        setLoading(false);
    }
  };

  const showToastMsg = (message: string) => {
      setToast(message);
      setTimeout(() => setToast(""), 5000);
  };

  const handleResetPassword = async (e: React.FormEvent) => {
      e.preventDefault();
      setLoading(true);
      try {
          const res = await fetch("http://localhost:8000/api/reset-password", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ email: resetEmail })
          });
          const data = await res.json();
          alert(`Your new password is: ${data.new_password}\n\nPlease login using this password.`);
          setShowResetModal(false);
      } catch (err) {
          alert("Failed to reset password.");
      }
      setLoading(false);
  };

  return (
    <div className="flex min-h-screen w-full items-center justify-center bg-[#F5F5F4] text-[#111111] p-4 font-sans relative">
      
      {/* Toast Notification */}
      <AnimatePresence>
      {toast && (
          <motion.div 
              initial={{ y: -50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: -50, opacity: 0 }}
              className="absolute top-8 left-1/2 -translate-x-1/2 bg-[#111111] text-white px-6 py-3 rounded-full shadow-xl z-50 text-sm font-medium"
          >
              {toast}
          </motion.div>
      )}
      </AnimatePresence>

      <AnimatePresence>
          {/* Reset Password Modal */}
          {showResetModal && (
              <motion.div 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="absolute inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm"
              >
                  <motion.div 
                      initial={{ scale: 0.95, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      exit={{ scale: 0.95, opacity: 0 }}
                      className="bg-white w-[400px] rounded-[18px] shadow-2xl p-8 flex flex-col"
                  >
                      <h2 className="text-xl font-semibold mb-1 text-[#111111]">Reset Password</h2>
                      <p className="text-sm text-[#6B7280] mb-6">Enter your email to receive a temporary password.</p>
                      
                      <form onSubmit={handleResetPassword} className="w-full space-y-4 mb-6">
                          <input 
                              type="email" 
                              value={resetEmail}
                              onChange={(e) => setResetEmail(e.target.value)}
                              placeholder="Email Address" 
                              className="w-full bg-[#F5F5F4] border border-[#E5E7EB] text-[#111111] placeholder-[#6B7280] rounded-xl px-4 py-3 focus:outline-none focus:ring-1 focus:ring-[#DC2626] transition-all text-sm font-medium"
                              required
                          />
                          <button 
                              type="submit" 
                              disabled={loading}
                              className="w-full bg-[#111111] hover:bg-black text-white font-bold py-3 px-4 rounded-xl transition-colors duration-200 text-sm disabled:opacity-50"
                          >
                              {loading ? "Processing..." : "Reset Password"}
                          </button>
                      </form>

                      <button type="button" onClick={() => setShowResetModal(false)} className="text-sm font-semibold text-[#6B7280] hover:text-[#111111] self-center">
                          Cancel
                      </button>
                  </motion.div>
              </motion.div>
          )}
      </AnimatePresence>

      {/* Main Container */}
      <div className="w-full max-w-[1000px] h-[650px] bg-white rounded-[24px] shadow-sm border border-[#E5E7EB] flex overflow-hidden">
        
        {/* Left Column: Image or Features */}
        <div className="hidden lg:block w-1/2 relative bg-[#111111] overflow-hidden">
            <AnimatePresence mode="wait">
                {!showFeatures ? (
                    <motion.div 
                        key="image-panel"
                        initial={{ opacity: 0, x: -50 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -50 }}
                        transition={{ duration: 0.5 }}
                        className="absolute inset-0 bg-cover bg-center"
                        style={{ backgroundImage: "url('/login-bg.png')" }}
                    >
                        <div className="absolute inset-0 bg-black/20"></div>
                        
                        {/* Top header on image */}
                        <div className="absolute top-8 left-8 flex justify-between text-white font-medium text-sm z-10">
                            <span>JOBX</span>
                        </div>

                        {/* Flip Button */}
                        <div className="absolute bottom-10 right-10 z-10">
                            <button 
                                onClick={() => setShowFeatures(true)} 
                                className="w-12 h-12 rounded-full bg-white/10 backdrop-blur-md border border-white/30 flex items-center justify-center text-white hover:bg-white/20 transition-all group"
                            >
                                <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
                            </button>
                        </div>
                    </motion.div>
                ) : (
                    <motion.div
                        key="features-panel"
                        initial={{ opacity: 0, x: 50 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 50 }}
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
                        <div className="absolute top-8 left-8">
                            <button 
                                onClick={() => setShowFeatures(false)} 
                                className="w-10 h-10 rounded-full border border-[#222] flex items-center justify-center text-white hover:bg-[#222] transition-all group"
                            >
                                <ArrowRight className="w-5 h-5 group-hover:-translate-x-1 transition-transform rotate-180" />
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>

        {/* Right Column: Login Form */}
        <div className="w-full lg:w-1/2 flex flex-col p-10 lg:p-14 relative bg-white">
          <div className="flex-1 flex flex-col justify-center max-w-[320px] mx-auto w-full">
              <h1 className="text-3xl font-bold text-[#111111] mb-2 tracking-tight">Login</h1>
              <p className="text-[#6B7280] text-sm font-medium mb-10">Welcome back to JOBX</p>

              {error && (
                  <div className="mb-6 p-3 bg-[#DC2626]/10 text-[#DC2626] text-sm font-medium rounded-xl text-center border border-[#DC2626]/20">
                      {error}
                  </div>
              )}

              <form onSubmit={handleAuth} className="space-y-4">
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
                          placeholder="Password" 
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

                  <div className="flex justify-end pt-1">
                      <button type="button" onClick={() => setShowResetModal(true)} className="text-xs font-semibold text-[#DC2626] hover:text-red-700 transition-colors">Forgot password ?</button>
                  </div>

                  <button 
                      type="submit" 
                      disabled={loading}
                      className="w-full bg-[#111111] hover:bg-black text-white font-bold py-3 px-4 rounded-xl mt-2 transition-colors duration-200 text-sm disabled:opacity-50"
                  >
                      {loading ? "Authenticating..." : "Login"}
                  </button>

                  <Link href="/register" className="w-full block text-center bg-white border border-[#E5E7EB] hover:bg-[#F5F5F4] text-[#111111] font-bold py-3 px-4 rounded-xl transition-colors duration-200 text-sm">
                      Create Account
                  </Link>
              </form>
          </div>
        </div>

      </div>
    </div>
  );
}

"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Settings, Shield, User, Save, Lock, Palette, Globe, Download, Trash2, Bell, AlertTriangle, X } from "lucide-react";
import Toast, { ToastType } from "@/components/Toast";
import { useRouter } from "next/navigation";

function getToken() {
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
        const [k, v] = c.trim().split('=');
        if (k === 'jobx_token') return v;
    }
    return null;
}

export default function SettingsPage() {
    const router = useRouter();
    
    // UI State
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [toast, setToast] = useState<{message: string, type: ToastType} | null>(null);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    
    // Profile State
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [initialState, setInitialState] = useState<any>({});
    
    // Password State
    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [changingPassword, setChangingPassword] = useState(false);

    // Preferences State
    const [strictMode, setStrictMode] = useState(true);
    const [autoDelete, setAutoDelete] = useState(false);
    const [theme, setTheme] = useState("system");
    const [language, setLanguage] = useState("en");
    const [emailAlerts, setEmailAlerts] = useState(true);
    const [fraudAlerts, setFraudAlerts] = useState(true);
    const [weeklyReports, setWeeklyReports] = useState(false);

    // Delete Account State
    const [deletePassword, setDeletePassword] = useState("");
    const [deleting, setDeleting] = useState(false);

    useEffect(() => {
        fetchSettings();
    }, []);

    const fetchSettings = async () => {
        const token = getToken();
        if (!token) {
            router.push("/login");
            return;
        }

        try {
            const res = await fetch("http://localhost:8000/api/me", {
                headers: { "Authorization": `Bearer ${token}` }
            });
            
            if (res.ok) {
                const data = await res.json();
                setName(data.name || "");
                setEmail(data.email || "");
                setStrictMode(data.strict_mode ?? false);
                setAutoDelete(data.auto_delete ?? false);
                setTheme(data.theme || "system");
                setLanguage(data.language || "en");
                setEmailAlerts(data.email_alerts ?? true);
                setFraudAlerts(data.fraud_alerts ?? true);
                setWeeklyReports(data.weekly_reports ?? false);
                
                // Track initial state to know if anything changed
                setInitialState(data);
            } else {
                setToast({ message: "Failed to load settings. Please log in again.", type: "error" });
            }
        } catch (e) {
            setToast({ message: "Network error while loading settings.", type: "error" });
        } finally {
            setLoading(false);
        }
    };

    const hasChanges = () => {
        if (!initialState.email) return true; // not loaded yet
        return name !== initialState.name ||
               email !== initialState.email ||
               strictMode !== initialState.strict_mode ||
               autoDelete !== initialState.auto_delete ||
               theme !== initialState.theme ||
               language !== initialState.language ||
               emailAlerts !== initialState.email_alerts ||
               fraudAlerts !== initialState.fraud_alerts ||
               weeklyReports !== initialState.weekly_reports;
    };

    const handleSavePreferences = async () => {
        if (!hasChanges()) {
            setToast({ message: "No changes to save.", type: "info" });
            return;
        }

        // Validate
        if (!name.trim()) return setToast({ message: "Name cannot be empty.", type: "error" });
        if (!email.includes("@")) return setToast({ message: "Invalid email address.", type: "error" });

        setSaving(true);
        const token = getToken();
        try {
            const res = await fetch("http://localhost:8000/api/settings", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    name, email,
                    strict_mode: strictMode,
                    auto_delete: autoDelete,
                    theme, language,
                    email_alerts: emailAlerts,
                    fraud_alerts: fraudAlerts,
                    weekly_reports: weeklyReports
                })
            });
            const data = await res.json();
            
            if (res.ok) {
                setToast({ message: "Preferences saved successfully!", type: "success" });
                fetchSettings(); // reload
            } else {
                setToast({ message: data.detail || "Failed to save preferences", type: "error" });
            }
        } catch (e) {
            setToast({ message: "Network failure.", type: "error" });
        } finally {
            setSaving(false);
        }
    };

    const handlePasswordChange = async () => {
        if (!currentPassword) return setToast({ message: "Enter current password.", type: "error" });
        if (newPassword.length < 8) return setToast({ message: "New password must be at least 8 characters.", type: "error" });
        if (newPassword !== confirmPassword) return setToast({ message: "Passwords do not match.", type: "error" });

        setChangingPassword(true);
        const token = getToken();
        try {
            const res = await fetch("http://localhost:8000/api/password", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    current_password: currentPassword,
                    new_password: newPassword
                })
            });
            const data = await res.json();
            
            if (res.ok) {
                setToast({ message: "Password updated successfully!", type: "success" });
                setCurrentPassword("");
                setNewPassword("");
                setConfirmPassword("");
            } else {
                setToast({ message: data.detail || "Failed to update password", type: "error" });
            }
        } catch (e) {
            setToast({ message: "Network failure.", type: "error" });
        } finally {
            setChangingPassword(false);
        }
    };

    const handleExport = async (type: string) => {
        const token = getToken();
        try {
            const res = await fetch(`http://localhost:8000/api/export/${type}`, {
                headers: { "Authorization": `Bearer ${token}` }
            });
            
            if (!res.ok) throw new Error();
            
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `jobx_export.${type}`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (e) {
            setToast({ message: "Failed to export data.", type: "error" });
        }
    };

    const handleClearData = async (type: string) => {
        if (!confirm(`Are you sure you want to delete all your ${type}? This cannot be undone.`)) return;

        const token = getToken();
        try {
            const res = await fetch(`http://localhost:8000/api/data/${type}`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (res.ok) {
                setToast({ message: `${type} deleted successfully!`, type: "success" });
            } else {
                setToast({ message: `Failed to delete ${type}`, type: "error" });
            }
        } catch (e) {
            setToast({ message: "Network failure.", type: "error" });
        }
    };

    const handleDeleteAccount = async () => {
        if (!deletePassword) return setToast({ message: "Password is required to delete account.", type: "error" });
        
        setDeleting(true);
        const token = getToken();
        try {
            const res = await fetch("http://localhost:8000/api/account", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ password: deletePassword })
            });
            const data = await res.json();
            
            if (res.ok) {
                document.cookie = "jobx_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
                router.push("/login");
            } else {
                setToast({ message: data.detail || "Failed to delete account", type: "error" });
            }
        } catch (e) {
            setToast({ message: "Network failure.", type: "error" });
        } finally {
            setDeleting(false);
        }
    };

    const handleLogout = async (allDevices: boolean) => {
        try {
            await fetch("http://localhost:8000/api/logout", { method: "POST" });
        } catch (e) {}
        document.cookie = "jobx_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
        router.push("/login");
    };

    if (loading) {
        return (
            <div className="w-full flex items-center justify-center py-20">
                <div className="w-8 h-8 border-2 border-[#111111] border-t-transparent rounded-full animate-spin"></div>
            </div>
        );
    }

    return (
        <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full flex flex-col gap-8 pb-10"
        >
            {toast && (
                <Toast 
                    message={toast.message} 
                    type={toast.type} 
                    onClose={() => setToast(null)} 
                />
            )}

            {/* Header */}
            <div className="flex justify-between items-center bg-[#FFFFFF] rounded-[18px] shadow-sm border border-[#E5E7EB] p-8">
                <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-[#F5F5F4] text-[#111111] rounded-lg border border-[#E5E7EB] flex items-center justify-center">
                        <Settings className="w-6 h-6" />
                    </div>
                    <div>
                        <h1 className="text-xl font-semibold text-[#111111] tracking-tight">System Settings</h1>
                        <p className="text-sm text-[#6B7280] mt-1">Manage your account and threat detection preferences.</p>
                    </div>
                </div>
            </div>

            {/* Profile Settings */}
            <div className="bg-[#FFFFFF] rounded-[18px] shadow-sm border border-[#E5E7EB] overflow-hidden">
                <div className="p-6 border-b border-[#E5E7EB] flex items-center gap-3">
                    <User className="w-5 h-5 text-[#6B7280]" />
                    <h2 className="text-sm font-semibold text-[#111111]">Profile Settings</h2>
                </div>
                <div className="p-8 space-y-6">
                    <div className="grid grid-cols-2 gap-6">
                        <div>
                            <label className="block text-xs font-semibold text-[#111111] mb-1.5">Full Name</label>
                            <input 
                                type="text" 
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                className="w-full bg-[#F5F5F4] border border-[#E5E7EB] rounded-lg px-4 py-2.5 text-sm focus:ring-1 focus:ring-[#111111] outline-none transition-all font-medium text-[#111111]" 
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-semibold text-[#111111] mb-1.5">Email Address</label>
                            <input 
                                type="email" 
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full bg-[#F5F5F4] border border-[#E5E7EB] rounded-lg px-4 py-2.5 text-sm focus:ring-1 focus:ring-[#111111] outline-none transition-all font-medium text-[#111111]" 
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* Password Management */}
            <div className="bg-[#FFFFFF] rounded-[18px] shadow-sm border border-[#E5E7EB] overflow-hidden">
                <div className="p-6 border-b border-[#E5E7EB] flex items-center gap-3">
                    <Lock className="w-5 h-5 text-[#6B7280]" />
                    <h2 className="text-sm font-semibold text-[#111111]">Password Management</h2>
                </div>
                <div className="p-8 space-y-6">
                    <div className="grid grid-cols-3 gap-6">
                        <div>
                            <label className="block text-xs font-semibold text-[#111111] mb-1.5">Current Password</label>
                            <input 
                                type="password" 
                                value={currentPassword}
                                onChange={(e) => setCurrentPassword(e.target.value)}
                                className="w-full bg-[#F5F5F4] border border-[#E5E7EB] rounded-lg px-4 py-2.5 text-sm focus:ring-1 focus:ring-[#111111] outline-none transition-all font-medium text-[#111111]" 
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-semibold text-[#111111] mb-1.5">New Password (8+ chars)</label>
                            <input 
                                type="password" 
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                className="w-full bg-[#F5F5F4] border border-[#E5E7EB] rounded-lg px-4 py-2.5 text-sm focus:ring-1 focus:ring-[#111111] outline-none transition-all font-medium text-[#111111]" 
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-semibold text-[#111111] mb-1.5">Confirm Password</label>
                            <input 
                                type="password" 
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                className="w-full bg-[#F5F5F4] border border-[#E5E7EB] rounded-lg px-4 py-2.5 text-sm focus:ring-1 focus:ring-[#111111] outline-none transition-all font-medium text-[#111111]" 
                            />
                        </div>
                    </div>
                    <div>
                        <button 
                            onClick={handlePasswordChange}
                            disabled={changingPassword}
                            className="bg-[#F5F5F4] hover:bg-[#E5E7EB] text-[#111111] border border-[#E5E7EB] font-medium py-2.5 px-5 rounded-lg transition-colors text-sm"
                        >
                            {changingPassword ? "Updating..." : "Update Password"}
                        </button>
                    </div>
                </div>
            </div>

            {/* Detection Preferences */}
            <div className="bg-[#FFFFFF] rounded-[18px] shadow-sm border border-[#E5E7EB] overflow-hidden">
                <div className="p-6 border-b border-[#E5E7EB] flex items-center gap-3">
                    <Shield className="w-5 h-5 text-[#6B7280]" />
                    <h2 className="text-sm font-semibold text-[#111111]">Detection Preferences</h2>
                </div>
                <div className="p-8 space-y-4">
                    <div 
                        onClick={() => setStrictMode(!strictMode)}
                        className="flex items-center justify-between p-4 bg-[#F5F5F4] rounded-xl border border-[#E5E7EB] cursor-pointer transition-colors hover:border-[#D1D5DB]"
                    >
                        <div>
                            <h3 className="font-semibold text-sm text-[#111111]">Strict Heuristics Mode</h3>
                            <p className="text-xs text-[#6B7280] mt-0.5">Increases risk score for any mentions of WhatsApp or Telegram.</p>
                        </div>
                        <div className={`w-12 h-6 rounded-full relative shadow-inner transition-colors ${strictMode ? 'bg-[#111111]' : 'bg-[#E5E7EB]'}`}>
                            <div className={`w-5 h-5 bg-white rounded-full absolute top-0.5 shadow-sm transition-all ${strictMode ? 'right-0.5' : 'left-0.5'}`}></div>
                        </div>
                    </div>
                    <div 
                        onClick={() => setAutoDelete(!autoDelete)}
                        className="flex items-center justify-between p-4 bg-[#F5F5F4] rounded-xl border border-[#E5E7EB] cursor-pointer transition-colors hover:border-[#D1D5DB]"
                    >
                        <div>
                            <h3 className="font-semibold text-sm text-[#111111]">Auto-Delete Safe Scans</h3>
                            <p className="text-xs text-[#6B7280] mt-0.5">Automatically remove logs of jobs classified as Low Risk after 30 days.</p>
                        </div>
                        <div className={`w-12 h-6 rounded-full relative shadow-inner transition-colors ${autoDelete ? 'bg-[#111111]' : 'bg-[#E5E7EB]'}`}>
                            <div className={`w-5 h-5 bg-white rounded-full absolute top-0.5 shadow-sm transition-all ${autoDelete ? 'right-0.5' : 'left-0.5'}`}></div>
                        </div>
                    </div>
                </div>
            </div>


            {/* Notifications */}
            <div className="bg-[#FFFFFF] rounded-[18px] shadow-sm border border-[#E5E7EB] overflow-hidden">
                <div className="p-6 border-b border-[#E5E7EB] flex items-center gap-3">
                    <Bell className="w-5 h-5 text-[#6B7280]" />
                    <h2 className="text-sm font-semibold text-[#111111]">Notifications</h2>
                </div>
                <div className="p-8 space-y-4">
                    <div 
                        onClick={() => setEmailAlerts(!emailAlerts)}
                        className="flex items-center justify-between p-4 bg-[#F5F5F4] rounded-xl border border-[#E5E7EB] cursor-pointer transition-colors hover:border-[#D1D5DB]"
                    >
                        <div>
                            <h3 className="font-semibold text-sm text-[#111111]">Email Alerts</h3>
                            <p className="text-xs text-[#6B7280] mt-0.5">Receive general account alerts and updates via email.</p>
                        </div>
                        <div className={`w-12 h-6 rounded-full relative shadow-inner transition-colors ${emailAlerts ? 'bg-[#111111]' : 'bg-[#E5E7EB]'}`}>
                            <div className={`w-5 h-5 bg-white rounded-full absolute top-0.5 shadow-sm transition-all ${emailAlerts ? 'right-0.5' : 'left-0.5'}`}></div>
                        </div>
                    </div>
                    <div 
                        onClick={() => setFraudAlerts(!fraudAlerts)}
                        className="flex items-center justify-between p-4 bg-[#F5F5F4] rounded-xl border border-[#E5E7EB] cursor-pointer transition-colors hover:border-[#D1D5DB]"
                    >
                        <div>
                            <h3 className="font-semibold text-sm text-[#111111]">Fraud Detection Alerts</h3>
                            <p className="text-xs text-[#6B7280] mt-0.5">Get notified immediately when you scan a High Risk job.</p>
                        </div>
                        <div className={`w-12 h-6 rounded-full relative shadow-inner transition-colors ${fraudAlerts ? 'bg-[#111111]' : 'bg-[#E5E7EB]'}`}>
                            <div className={`w-5 h-5 bg-white rounded-full absolute top-0.5 shadow-sm transition-all ${fraudAlerts ? 'right-0.5' : 'left-0.5'}`}></div>
                        </div>
                    </div>
                    <div 
                        onClick={() => setWeeklyReports(!weeklyReports)}
                        className="flex items-center justify-between p-4 bg-[#F5F5F4] rounded-xl border border-[#E5E7EB] cursor-pointer transition-colors hover:border-[#D1D5DB]"
                    >
                        <div>
                            <h3 className="font-semibold text-sm text-[#111111]">Weekly Report Emails</h3>
                            <p className="text-xs text-[#6B7280] mt-0.5">Receive a summary of your scan history and analytics every week.</p>
                        </div>
                        <div className={`w-12 h-6 rounded-full relative shadow-inner transition-colors ${weeklyReports ? 'bg-[#111111]' : 'bg-[#E5E7EB]'}`}>
                            <div className={`w-5 h-5 bg-white rounded-full absolute top-0.5 shadow-sm transition-all ${weeklyReports ? 'right-0.5' : 'left-0.5'}`}></div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Export Settings */}
            <div className="bg-[#FFFFFF] rounded-[18px] shadow-sm border border-[#E5E7EB] overflow-hidden">
                <div className="p-6 border-b border-[#E5E7EB] flex items-center gap-3">
                    <Download className="w-5 h-5 text-[#6B7280]" />
                    <h2 className="text-sm font-semibold text-[#111111]">Export Data</h2>
                </div>
                <div className="p-8">
                    <div className="flex flex-wrap gap-4">
                        <button onClick={() => handleExport('json')} className="bg-[#F5F5F4] hover:bg-[#E5E7EB] border border-[#E5E7EB] text-[#111111] font-medium py-2.5 px-5 rounded-lg transition-colors text-sm flex items-center gap-2">
                            <Download className="w-4 h-4" /> Export My Data (JSON)
                        </button>
                        <button onClick={() => handleExport('csv')} className="bg-[#F5F5F4] hover:bg-[#E5E7EB] border border-[#E5E7EB] text-[#111111] font-medium py-2.5 px-5 rounded-lg transition-colors text-sm flex items-center gap-2">
                            <Download className="w-4 h-4" /> Export Scan History (CSV)
                        </button>
                        <button onClick={() => handleExport('pdf')} className="bg-[#F5F5F4] hover:bg-[#E5E7EB] border border-[#E5E7EB] text-[#111111] font-medium py-2.5 px-5 rounded-lg transition-colors text-sm flex items-center gap-2">
                            <Download className="w-4 h-4" /> Export Scan History (PDF)
                        </button>
                    </div>
                </div>
            </div>

            {/* Data Management */}
            <div className="bg-[#FFFFFF] rounded-[18px] shadow-sm border border-[#E5E7EB] overflow-hidden">
                <div className="p-6 border-b border-[#E5E7EB] flex items-center gap-3">
                    <Trash2 className="w-5 h-5 text-[#6B7280]" />
                    <h2 className="text-sm font-semibold text-[#111111]">Data Management</h2>
                </div>
                <div className="p-8">
                    <div className="flex flex-wrap gap-4">
                        <button onClick={() => handleClearData('scans')} className="bg-[#FEF2F2] hover:bg-[#FEE2E2] border border-[#FECACA] text-[#DC2626] font-medium py-2.5 px-5 rounded-lg transition-colors text-sm flex items-center gap-2">
                            <Trash2 className="w-4 h-4" /> Clear Scan History
                        </button>
                        <button onClick={() => setShowDeleteModal(true)} className="bg-[#DC2626] hover:bg-[#B91C1C] text-white font-medium py-2.5 px-5 rounded-lg transition-colors text-sm flex items-center gap-2">
                            <AlertTriangle className="w-4 h-4" /> Delete Account
                        </button>
                    </div>
                </div>
            </div>



            {/* Save Button */}
            <div className="flex justify-end sticky bottom-8 z-10">
                <button 
                    onClick={handleSavePreferences}
                    disabled={saving}
                    className="flex items-center gap-2 bg-[#111111] hover:bg-black text-white font-medium py-3 px-8 rounded-xl shadow-lg transition-all text-sm disabled:opacity-50"
                >
                    <Save className="w-4 h-4" /> {saving ? "Saving..." : "Save Preferences"}
                </button>
            </div>

            {/* Delete Account Modal */}
            <AnimatePresence>
                {showDeleteModal && (
                    <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
                        <motion.div 
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="bg-white rounded-2xl p-8 max-w-md w-full shadow-2xl relative"
                        >
                            <button 
                                onClick={() => setShowDeleteModal(false)}
                                className="absolute top-4 right-4 text-[#6B7280] hover:text-[#111111]"
                            >
                                <X className="w-5 h-5" />
                            </button>
                            
                            <div className="w-12 h-12 bg-[#FEF2F2] rounded-full flex items-center justify-center mb-6">
                                <AlertTriangle className="w-6 h-6 text-[#DC2626]" />
                            </div>
                            
                            <h3 className="text-xl font-bold text-[#111111] mb-2">Delete Account</h3>
                            <p className="text-sm text-[#6B7280] mb-6">
                                This action is permanent and cannot be undone. All your scan history, reports, analytics, and personal data will be completely erased.
                            </p>
                            
                            <div className="space-y-4 mb-8">
                                <div>
                                    <label className="block text-xs font-semibold text-[#111111] mb-1.5">Enter Password to Confirm</label>
                                    <input 
                                        type="password" 
                                        value={deletePassword}
                                        onChange={(e) => setDeletePassword(e.target.value)}
                                        placeholder="Current Password"
                                        className="w-full bg-[#F5F5F4] border border-[#E5E7EB] rounded-lg px-4 py-2.5 text-sm focus:ring-1 focus:ring-[#DC2626] outline-none transition-all font-medium text-[#111111]" 
                                    />
                                </div>
                            </div>
                            
                            <div className="flex gap-4">
                                <button 
                                    onClick={() => setShowDeleteModal(false)}
                                    className="flex-1 bg-[#F5F5F4] hover:bg-[#E5E7EB] text-[#111111] font-medium py-3 rounded-xl transition-colors text-sm"
                                >
                                    Cancel
                                </button>
                                <button 
                                    onClick={handleDeleteAccount}
                                    disabled={deleting}
                                    className="flex-1 bg-[#DC2626] hover:bg-[#B91C1C] text-white font-medium py-3 rounded-xl transition-colors text-sm"
                                >
                                    {deleting ? "Deleting..." : "Permanently Delete"}
                                </button>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

        </motion.div>
    );
}

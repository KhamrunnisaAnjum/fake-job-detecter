"use client";

import { FiUser, FiMoon, FiBell, FiLock } from "react-icons/fi";

export default function SettingsPage() {
  return (
    <div className="min-h-screen bg-[#F6F7FB] p-10">
      <div className="max-w-5xl mx-auto">
        <p className="uppercase tracking-[4px] text-sm text-neutral-500">
          JobX
        </p>

        <h1 className="mt-2 text-5xl font-bold">Settings</h1>

        <div className="mt-10 space-y-6">
          <div className="rounded-3xl bg-white p-6 shadow-sm flex justify-between items-center">
            <div className="flex gap-4 items-center">
              <FiUser size={24} />
              <div>
                <h2 className="font-bold">Profile</h2>
                <p className="text-neutral-500">Manage your account</p>
              </div>
            </div>
            <button className="bg-black text-white px-5 py-2 rounded-xl">
              Edit
            </button>
          </div>

          <div className="rounded-3xl bg-white p-6 shadow-sm flex justify-between items-center">
            <div className="flex gap-4 items-center">
              <FiMoon size={24} />
              <div>
                <h2 className="font-bold">Dark Mode</h2>
                <p className="text-neutral-500">Coming Soon</p>
              </div>
            </div>

            <input type="checkbox" />
          </div>

          <div className="rounded-3xl bg-white p-6 shadow-sm flex justify-between items-center">
            <div className="flex gap-4 items-center">
              <FiBell size={24} />
              <div>
                <h2 className="font-bold">Notifications</h2>
                <p className="text-neutral-500">Email Alerts</p>
              </div>
            </div>

            <input type="checkbox" defaultChecked />
          </div>

          <div className="rounded-3xl bg-white p-6 shadow-sm flex justify-between items-center">
            <div className="flex gap-4 items-center">
              <FiLock size={24} />
              <div>
                <h2 className="font-bold">Password</h2>
                <p className="text-neutral-500">Change Password</p>
              </div>
            </div>

            <button className="bg-black text-white px-5 py-2 rounded-xl">
              Change
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

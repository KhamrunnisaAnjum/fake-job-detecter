"use client";

import { FiSearch, FiDownload } from "react-icons/fi";

const history = [
  {
    company: "Google",
    role: "Frontend Developer",
    risk: "Safe",
    date: "Today",
  },
  {
    company: "Amazon",
    role: "Backend Engineer",
    risk: "Safe",
    date: "Yesterday",
  },
  {
    company: "Unknown Recruiter",
    role: "Remote Data Entry",
    risk: "High",
    date: "2 Days Ago",
  },
  {
    company: "Microsoft",
    role: "Software Engineer",
    risk: "Safe",
    date: "3 Days Ago",
  },
  {
    company: "Fake HR Pvt Ltd",
    role: "Work From Home",
    risk: "Medium",
    date: "4 Days Ago",
  },
];

export default function HistoryPage() {
  return (
    <div className="min-h-screen bg-[#F6F7FB] p-10">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between">
          <div>
            <p className="uppercase tracking-[4px] text-sm text-neutral-500">
              JobX
            </p>

            <h1 className="mt-2 text-5xl font-bold">My History</h1>
          </div>

          <button className="flex items-center gap-2 rounded-2xl bg-black px-6 py-3 text-white">
            <FiDownload />
            Export
          </button>
        </div>

        <div className="mt-8 rounded-2xl bg-white p-5 shadow-sm">
          <div className="relative">
            <FiSearch className="absolute left-4 top-4 text-neutral-500" />

            <input
              placeholder="Search previous scans..."
              className="w-full rounded-xl border py-3 pl-12 pr-4 outline-none focus:border-black"
            />
          </div>
        </div>

        <div className="mt-8 overflow-hidden rounded-3xl bg-white shadow-sm">
          <table className="w-full">
            <thead className="bg-neutral-100">
              <tr>
                <th className="p-5 text-left">Company</th>
                <th className="text-left">Role</th>
                <th className="text-left">Risk</th>
                <th className="text-left">Date</th>
              </tr>
            </thead>

            <tbody>
              {history.map((item, index) => (
                <tr key={index} className="border-t hover:bg-neutral-50">
                  <td className="p-5 font-semibold">{item.company}</td>

                  <td>{item.role}</td>

                  <td>
                    <span
                      className={`rounded-full px-4 py-2 text-sm font-semibold

                      ${
                        item.risk === "Safe"
                          ? "bg-green-100 text-green-700"
                          : item.risk === "Medium"
                            ? "bg-yellow-100 text-yellow-700"
                            : "bg-red-100 text-red-700"
                      }

                      `}
                    >
                      {item.risk}
                    </span>
                  </td>

                  <td>{item.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

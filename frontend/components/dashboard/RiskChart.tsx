import { FiShield } from "react-icons/fi";

export default function RiskChart() {
  return (
    <div className="rounded-3xl border border-neutral-200 bg-white p-7 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-neutral-500">Risk Distribution</p>

          <h2 className="mt-2 text-2xl font-bold">Threat Analysis</h2>
        </div>

        <div className="rounded-2xl bg-red-50 p-3">
          <FiShield className="text-red-500" size={24} />
        </div>
      </div>

      <div className="mt-10 space-y-6">
        <div>
          <div className="mb-2 flex justify-between text-sm">
            <span>Low Risk</span>
            <span>78%</span>
          </div>

          <div className="h-3 rounded-full bg-neutral-200">
            <div className="h-3 w-[78%] rounded-full bg-green-500"></div>
          </div>
        </div>

        <div>
          <div className="mb-2 flex justify-between text-sm">
            <span>Medium Risk</span>
            <span>15%</span>
          </div>

          <div className="h-3 rounded-full bg-neutral-200">
            <div className="h-3 w-[15%] rounded-full bg-yellow-500"></div>
          </div>
        </div>

        <div>
          <div className="mb-2 flex justify-between text-sm">
            <span>High Risk</span>
            <span>7%</span>
          </div>

          <div className="h-3 rounded-full bg-neutral-200">
            <div className="h-3 w-[7%] rounded-full bg-red-500"></div>
          </div>
        </div>
      </div>
    </div>
  );
}

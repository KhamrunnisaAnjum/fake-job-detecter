import {
  FiActivity,
  FiShield,
  FiAlertTriangle,
  FiTrendingUp,
} from "react-icons/fi";

const stats = [
  {
    title: "Jobs Scanned",
    value: "15,482",
    icon: FiActivity,
    color: "bg-blue-50 text-blue-600",
    change: "+12%",
  },
  {
    title: "Safe Jobs",
    value: "14,201",
    icon: FiShield,
    color: "bg-green-50 text-green-600",
    change: "+8%",
  },
  {
    title: "Fake Jobs",
    value: "1,281",
    icon: FiAlertTriangle,
    color: "bg-red-50 text-red-600",
    change: "-3%",
  },
  {
    title: "Detection Accuracy",
    value: "98%",
    icon: FiTrendingUp,
    color: "bg-purple-50 text-purple-600",
    change: "+1%",
  },
];

export default function Stats() {
  return (
    <section className="mt-8 grid grid-cols-4 gap-6">
      {stats.map((item) => {
        const Icon = item.icon;

        return (
          <div
            key={item.title}
            className="group rounded-3xl border border-neutral-200 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
          >
            <div className="flex items-center justify-between">
              <div
                className={`flex h-14 w-14 items-center justify-center rounded-2xl ${item.color}`}
              >
                <Icon size={24} />
              </div>

              <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-600">
                {item.change}
              </span>
            </div>

            <h2 className="mt-8 text-4xl font-bold text-neutral-900">
              {item.value}
            </h2>

            <p className="mt-2 text-neutral-500">{item.title}</p>
          </div>
        );
      })}
    </section>
  );
}

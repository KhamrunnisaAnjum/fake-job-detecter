import Sidebar from "./Sidebar";
import Header from "./Header";
import Hero from "./Hero";
import Stats from "./Stats";
import RiskChart from "./RiskChart";
import ThreatGraph from "./ThreatGraph";
import RecentScans from "./RecentScans";

export default function DashboardLayout() {
  return (
    <div className="min-h-screen bg-[#F6F7FB] flex">
      <Sidebar />

      <main className="flex-1 p-8">
        <Header />

        <Hero />

        <Stats />

        <div className="grid grid-cols-2 gap-6 mt-8">
          <RiskChart />
          <ThreatGraph />
        </div>

        <div className="mt-8">
          <RecentScans />
        </div>
      </main>
    </div>
  );
}

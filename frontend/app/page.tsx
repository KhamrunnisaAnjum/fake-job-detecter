<<<<<<< HEAD
import LoginCard from "@/components/auth/LoginCard";
import LoginPanel from "@/components/auth/LoginPanel";

export default function Home() {
  return (
    <main className="min-h-screen bg-neutral-900 flex items-center justify-center p-8">
      <div className="w-full max-w-7xl h-[750px] rounded-[30px] overflow-hidden shadow-2xl grid grid-cols-2">
        <LoginCard />

        <LoginPanel />
      </div>
    </main>
  );
=======
import { redirect } from "next/navigation";

export default function Home() {
  redirect("/dashboard");
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6
}

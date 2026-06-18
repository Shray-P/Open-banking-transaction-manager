import { Outlet } from "react-router";
import "./Layout.css";
import { Navbar } from "./components/Navbar"

export function Layout() {
  return (
    <div className={"Layout"}>
      <header>
        <Navbar />
      </header>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}

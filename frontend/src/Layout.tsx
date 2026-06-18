import { Outlet } from "react-router";
import "./Layout.css";

export function Layout() {
  return (
    <div className={"Layout"}>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}

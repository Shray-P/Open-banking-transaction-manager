import { Link } from "react-router-dom";
import "./Navbar.css";

const pageLinks: [string, string][] = [
  ["/", "Home"],
  ["/login", "Login"]
];

export function Navbar() {
  return <nav className={"navbar"}>
    <ul className="navbar-links">
      {pageLinks.map(([path, name]) => (
        <li key={path}>
          <Link to={path}>
            {name}
          </Link>
        </li>
      ))}
    </ul>
  </nav>

}

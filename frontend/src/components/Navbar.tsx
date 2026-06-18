import { Link } from "react-router-dom";
import "./Navbar.css";

const pageLinks: [string, string][] = [
  ["/", "Home"],
];

export function Navbar() {
  return <nav className={"Navbar"}>
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

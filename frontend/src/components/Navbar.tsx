import { NavLink } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="navbar" role="navigation" aria-label="Main navigation">
      <div className="container navbar__inner">
        {/* Logo */}
        <NavLink to="/" className="navbar__logo" id="nav-logo">
          <div className="navbar__logo-icon" aria-hidden="true">🏛️</div>
          <span>Civic<span>Pulse</span></span>
        </NavLink>

        {/* Links */}
        <ul className="navbar__links" role="list">
          <li>
            <NavLink
              to="/submit"
              id="nav-submit"
              className={({ isActive }) =>
                'navbar__link' + (isActive ? ' active' : '')
              }
            >
              Submit
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/dashboard"
              id="nav-dashboard"
              className={({ isActive }) =>
                'navbar__link' + (isActive ? ' active' : '')
              }
            >
              Dashboard
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/stats"
              id="nav-stats"
              className={({ isActive }) =>
                'navbar__link' + (isActive ? ' active' : '')
              }
            >
              Stats
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
}

import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <header>
      <Link to="/" className="home-button">
        Home
      </Link>
      {/* other header content */}
    </header>
  );
}

export default Home;

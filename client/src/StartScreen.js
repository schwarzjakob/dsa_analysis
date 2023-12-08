import React from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';
import Header from './Header.js';

function StartScreen() {
  const navigate = useNavigate();

  return (
    <>
      <div>
        <Header />
      </div>
      <div className="start-container">
        {/* Welcoming Section */}
        <section className="welcome-section">
          <h1>Welcome to DSA Character Analyzer</h1>
          <p>Discover the depths of your characters in the world of Das Schwarze Auge.</p>
          <button onClick={() => navigate('/upload')}>Upload a Chatlog</button>
        </section>

        {/* Purpose and Features Section */}
        <section className="purpose-section">
          <h2>What We Offer</h2>
          <p>Explore talent usage, track character development, and dive into the detailed analysis of your DSA adventures.</p>
        </section>

        {/* DSA Background Section */}
        <section className="background-section">
          <h2>About Das Schwarze Auge</h2>
          <p>DSA is a classic fantasy role-playing game, rich with lore and adventure. Dive into a world of magic, mystery, and intrigue.</p>
        </section>

        {/* Character Highlights Section */}
        <section className="character-highlights">
          <h2>Character Highlights</h2>
          <div className="character-cards-container">
            {/* Placeholder for character cards */}
          </div>
        </section>

        {/* Call to Action */}
        <section className="cta-section">
          <button onClick={() => navigate('/talents/<character_name>')}>Explore Characters</button>
        </section>
      </div>
    </>
  );
}

export default StartScreen;

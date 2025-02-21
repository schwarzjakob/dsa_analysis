# DSA Rolls Analysis Web Application

## Overview

The DSA Rolls Analysis Web Application is a powerful tool designed to analyze and visualize character data from The Dark Eye (DSA) role-playing game. With a user-friendly interface built with React and Chart.js, and a robust backend powered by Python, this application offers detailed insights into character performance, traits, and fight metrics, enabling players to make informed decisions and track their progress over time.

## Key Features

- **Chatlog Upload & Analysis:** Easily upload your DSA chatlogs for in-depth analysis of your characters.
- **Interactive Data Visualization:** Explore character traits, categories, talents, and fight metrics through interactive charts.
- **Performance Tracking:** Analyze character performance over time using dynamic line charts.
- **Statistics Overview:** View simple statistics such as averages, successes, and failures for skill monitoring.
- **Efficient Data Processing:** Benefit from fast data fetching and processing powered by a Python-based backend.

## Installation and Setup

### Database Setup

1. **Install and Run PostgreSQL:**

   ```bash
   brew install postgresql@14
   brew services start postgresql@14
   psql postgres
   ```

2. **Install and Setup Database:**

   ```sql
   CREATE DATABASE dsa_analysis;
   CREATE USER dsa_user WITH PASSWORD 'dsa_user';
   ALTER ROLE dsa_user SET client_encoding TO 'utf8';
   ALTER ROLE dsa_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE dsa_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE dsa_analysis TO dsa_user;
   \q
   ```

3. **Install and Setup Schema:**

Don't forget to setup the DATABASE_URL in your `.env` file before continuing.

```bash
# DSA 4 / Roll 20
psql -U dsa_user -d dsa_analysis -f database/dsa4/schema.sql
psql -U dsa_user -d dsa_analysis -f database/dsa4/talents_spells_and_attacks.sql
psql -U dsa_user -d dsa_analysis -f database/dsa4/characters.sql

# DSA 5 / Foundry
psql -U dsa_user -d dsa_analysis -f database/dsa5/schema.sql
```

To retrieve data from foundry, I currently use a manual approach with JavaScript scripts in the browsers console and the insert script after creating the database.

### Backend Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/AixPrime/dsa_analysis.git
   cd dsa_rolls_webapp
   ```

2. **Setup the Python Flask Backend:**

   ```bash
   cd backend
   # Create a virtual environment (Linux/Mac)
   python3 -m venv venv
   source venv/bin/activate
   # For Windows
   python -m venv venv
   venv\Scripts\activate
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**
   Create a `.env` file in the `backend` directory and add the following lines to it:

   ```bash
   DATABASE_URL=postgresql://dsa_user:password@localhost:5432/dsa_analysis
   POSTGRES_DB=dsa_analysis
   POSTGRES_USER=dsa_user
   POSTGRES_PASSWORD=dsa_user
   ```

4. **Start the Flask Server:**

   ```bash
   python backend.py
   ```

### Frontend Setup

1. **Navigate to the Client Directory:**

   ```bash
   cd ../client
   ```

2. **Install Node.js Dependencies:**

   ```bash
   npm install
   ```

3. **Start the React Client:**

   ```bash
   npm start
   ```

   The client should now be running and accessible at `http://localhost:3000`.

## Current Issues

- Refine dsa5 foundry scripts to extract **relevant** data only
- Create database and ingest sample data
- Build MVP
  - Design Landing Page (What must an overview page have, Navbar, Group Analysis, Character Analysis)
  - Create Group Analysis page with some charts for analysis
  - Create Character Analysis page with some charts for analysis
- Review and potentially host and integrate into foundry (module for data retreival)
  - Implement login to scale application for different groups

## Ideas

### Analysis

- Talent Boxplots sortable after quartiles, mean, max, succes-rate etc.
- Collapsible Content: Show e.g. Talents only if interested, below spells with the same charts if applicable

### Bugs (dsa4 version)

- Aliases not displayed properly
- Categories in distribution include N/A (potentially spells, traits, etc.)

## DSA Forum Thread (German)

For more information or to join the discussion, visit the DSA Forum: [Kreative Ideen für Datenanalyse in DSA gesucht](https://dsaforum.de/viewtopic.php?p=2130810&sid=35430a31d27d49c3c592265d31acf1e0#p2130810)

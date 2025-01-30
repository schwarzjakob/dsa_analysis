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
psql -U dsa_user -d dsa_analysis -f database/schema.sql
psql -U dsa_user -d dsa_analysis -f database/talents_spells_and_attacks.sql
psql -U dsa_user -d dsa_analysis -f database/characters.sql
```

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
   python server.py
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

## Project Roadmap

### Objective

The primary goal of this project is to create a robust and modular analysis tool that not only processes DSA chat logs but also evolves into a platform capable of supporting multiple player groups and advanced data analysis.

### Phases

1. **Database Migration:**

   - **Transition to PostgreSQL:** Move from file-based storage to a PostgreSQL database hosted on neon.tech. This migration will ensure data integrity and scalability, enabling the application to handle large datasets and incremental updates without data loss.

2. **Data Parsing Enhancement:**

   - **HTML-Based Parsing:** Upgrade the data parsing script to extract information from HTML logs rather than plain text. This will allow for more accurate data capture, including timestamps, and prevent duplicate data entries.

3. **Modular Frontend Development:**

   - **Component-Based Architecture:** Refactor the React frontend into reusable components, focusing on maintainability and future enhancements. Unnecessary features, such as Google Authentication, will be removed or re-evaluated for future use.

4. **API Development:**

   - **RESTful API Design:** Implement a RESTful API to manage communication between the frontend and backend, supporting features like data fetching, filtering, and real-time updates.

5. **Scalability Preparation:**
   - **Multi-Tenancy Support:** Design the application to support multiple player groups, allowing for broader data collection and analysis.
   - **Advanced Analytics & Machine Learning:** Lay the groundwork for future machine learning projects by ensuring data is collected and stored in a format suitable for advanced analysis.

## DSA Forum Thread (German)

For more information or to join the discussion, visit the DSA Forum: [Kreative Ideen für Datenanalyse in DSA gesucht](https://dsaforum.de/viewtopic.php?p=2130810&sid=35430a31d27d49c3c592265d31acf1e0#p2130810)

## Ideas

- Refactor backend
  1. Database Service ✅
  2. Chatlog preprocessing microservice 🚧
     - It kind of works but the `chat_log_event_processor.py` does not utilize the database service. However I realize this may not be the ideal solution.

```
backend/
├── services/
│   ├── chat_preprocessing.py          # High-level orchestration (Step 1, 2, 3, 4, 5)
│   ├── chat_preprocessing/            # Subfolder for components
│   │   ├── parser/
│   │   │   ├── chat_parser.py         # Handles parsing logic
│   │   ├── validator/
│   │   │   ├── chat_validator.py      # Handles validation logic
│   ├── database_service.py            # Handles database interactions
│   ├── character_analysis.py          # Handles character analysis like talents, attacks, and trait usage logic
│   ├── exploratory_analysis.py        # Handles additional exploratory analysis (like formerly traits_needed_for_some_talents.py)
│   ├── roll_result_service.py         # Tbd.
├── models/
│   ├── game.py                 # Contains all DSA-related data models
│   ├── database.py             # Defines database models (if using SQLAlchemy)
├── utils/
│   ├── logging.py                     # Handles centralized logging
├── server.py
├── requirements.txt
├── uploads/
│   ├── chatlog.txt
```

- Talent Boxplots sortable after quartiles, mean, max, succes-rate etc.
- Collapsible Content: Show e.g. Talents only if interested, below spells with the same charts if applicable

### Bugs

- Aliases not displayed properly
- Categories in distribution include N/A (potentially spells, traits, etc.)

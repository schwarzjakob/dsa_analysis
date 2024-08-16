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

### Backend Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/AixPrime/dsa_analysis.git
   cd dsa_rolls_webapp
   ```

2. **Setup the Python Flask Backend:**
   ```bash
   cd flask-server
   # Create a virtual environment (Linux/Mac)
   python3 -m venv venv 
   source venv/bin/activate
   # For Windows
   python -m venv venv
   venv\Scripts\activate
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Start the Flask Server:**
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
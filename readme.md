# DSA Rolls Analysis Web Application

## Overview

This web application is designed for detailed analysis and visualization of character data in the context of DSA (The Dark Eye) role-playing game. It features interactive data visualization using React and Chart.js, and a backend built with Python for data processing.

## Features

- Upload your chatlog to analyze your characters
- Interactive data visualization of character traits, categories, talents and fight metrics.
- Analysis of character performance over time with line charts.
- Simple statistics for talents, and fight metrics such as averages, successes, and failures for skill monitoring.
- Efficient data fetching and processing from a Python backend.

## Installation and Setup

1. **Clone the repository:**
   
```bash
git clone https://https://github.com/AixPrime/dsa_analysis.git
cd dsa_rolls_webapp
cd flask-server
```


2. **Setup the virtual environment, and install requirements**
```bash
cd flask-server
# Linux/Mac
python3 -m venv venv 
source venv/bin/activate
# Windows
venv\Scripts\activate
python -m venv venv
pip install -r requirements.txt
```

3. **Start server and client**
```bash
python3 server.py
cd ..
cd /client
npm start
```

### Dsa Forum Thread (German)

[Kreative Ideen für Datenanalyse in DSA gesucht](https://dsaforum.de/viewtopic.php?p=2130810&sid=35430a31d27d49c3c592265d31acf1e0#p2130810)
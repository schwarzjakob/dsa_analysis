# DSA Rolls Analysis Web Application

## Overview

This web application is designed for detailed analysis and visualization of character data in the context of DSA (The Dark Eye) role-playing game. It features interactive data visualization using React and Chart.js, and a backend built with Python for data processing.

## Features

- Upload your chatlog to analyze your characters
- Interactive data visualization of character traits and talents.
- Analysis of character performance over time with line charts.
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
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

3. **Start server and client**

```bash
python3 server.py
cd ..
cd /client
npm start
```

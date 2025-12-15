# HL-Guarded-Biometric-Engine

A fully local, Python-based healthcare analytics application built for academic use. The app combines **cybersecurity**, **healthcare computation**, and **data analysis** into a single desktop GUI. All data is stored locally, no web services, no cloud dependencies.

## Overview

The application allows users to securely register and log in, compute various health and fitness metrics, store results over time, visualize progress through historical graphs, and manage (view/delete) past records.

The project is designed to demonstrate:

* Secure credential handling (hashing + salting)
* Local database management (SQLite)
* GUI development (Tkinter)
* Data visualization (Matplotlib)
* Applied healthcare calculations

## Features

### Authentication (Cybersecurity)

* Local user registration and login
* Password hashing using PBKDF2 (SHA-256 + salt)
* No plaintext password storage

### Fitness Calculators (Tracked Over Time)

These metrics are saved to the database and visualized on historical graphs:

* BMI (Body Mass Index)
* FFMI (Fat-Free Mass Index)
* Body Fat Percentage (US Navy method)
* VO2 Max (Cooper test)

Each metric can be viewed independently and tracked across multiple entries.

### Accessory Calculators (Not Tracked)

One-off calculators intended for immediate reference:

* BMR (Mifflin–St Jeor equation)
* TDEE (based on activity multiplier)

### Historical Graphs & Data Management

* Interactive graphs per metric
* Stable index-based timelines (no timestamp glitches)
* Table view of all past fitness entries
* Ability to delete individual records

## Tech Stack

* Python 3.13
* Tkinter (GUI)
* SQLite (local database)
* Matplotlib (data visualization)

## Project Structure

```
healthcare_app.py
/data
  └── app.db        # SQLite database (auto-generated)
```

## Setup & Usage

1. Install dependencies:

   ```
   pip install matplotlib
   ```

2. Run the application:

   ```
   python healthcare_app.py
   ```

3. Register a new user.

4. Log in and start using the calculators.

To reset the app (fresh database):

* Delete `data/app.db` while the app is closed.

## Academic Context

This project was developed as a **computer science semester project**, integrating multiple CS domains into a cohesive, practical system. The focus is on correctness, security, and local-first design rather than production deployment.

## Disclaimer

This application is for **educational purposes only** and does not provide medical advice.


# Secure Healthcare Analytics Platform

A Python desktop application developed as a first-year computer science project that combines secure user authentication, healthcare analytics, database management, and data visualization within a single local-first system.

The project was designed to explore practical software engineering concepts including cybersecurity fundamentals, GUI development, persistent data storage, and analytical data processing.

## Project Overview

This application allows users to:

* Register and authenticate securely
* Store and manage personal fitness records
* Calculate key health and performance metrics
* Track progress over time
* Visualize historical trends through graphs
* Manage stored records through a graphical interface

All functionality operates locally using SQLite, with no cloud services or external APIs.

## Technical Highlights

### Secure Authentication System

Implemented a complete user authentication workflow featuring:

* User registration and login
* PBKDF2-HMAC-SHA256 password hashing
* Random cryptographic salt generation
* Secure password verification using constant-time comparison
* No plaintext password storage

### Database Management

Designed and implemented a local SQLite database system for:

* User account management
* Persistent storage of fitness records
* Historical data retrieval
* Record deletion and management

### Desktop Application Development

Built a multi-window desktop application using Tkinter featuring:

* Authentication screens
* Dashboard navigation
* Calculator interfaces
* Historical data management
* Interactive graph visualization

### Data Analysis & Visualization

Implemented analytical features using Matplotlib to:

* Track fitness metrics over time
* Generate historical progress graphs
* Visualize trends across multiple measurements

## Health & Fitness Metrics

### Tracked Metrics

The following metrics are calculated, stored, and visualized:

* Body Mass Index (BMI)
* Fat-Free Mass Index (FFMI)
* Body Fat Percentage (US Navy Method)
* VO₂ Max (Cooper Test)

### Reference Calculators

Additional calculations include:

* Basal Metabolic Rate (BMR)
* Total Daily Energy Expenditure (TDEE)

## Technology Stack

* Python 3
* Tkinter
* SQLite
* Matplotlib

## Key Learning Outcomes

Through this project, I gained practical experience with:

* Authentication and access control systems
* Password hashing and credential security
* Database schema design
* SQL and SQLite integration
* GUI development
* Data visualization
* Software architecture and code organization
* Debugging and testing workflows

## Future Improvements

Potential future enhancements include:

* Improved UI/UX design
* Data export functionality
* Expanded analytics and reporting
* Automated testing
* Cross-platform packaging and deployment

## Project Structure

```text
healthcare_app.py
/data
  └── app.db
```

* `healthcare_app.py` contains the application logic, authentication system, database interactions, calculators, and GUI.
* `app.db` is the SQLite database automatically generated during execution and used for storing user accounts and fitness records.

## Setup & Usage

### Prerequisites

* Python 3.x
* Matplotlib

### Installation

Install the required dependency:

```bash
pip install matplotlib
```

### Running the Application

Launch the application using:

```bash
python healthcare_app.py
```

### Getting Started

1. Register a new user account.
2. Log in using your credentials.
3. Access the available fitness and health calculators.
4. Save fitness records to the database.
5. View historical trends through interactive graphs.
6. Manage stored records through the application interface.

### Database Reset

To start with a fresh database:

1. Close the application.
2. Delete the file:

```text
data/app.db
```

3. Restart the application.

A new database will be created automatically.

## Disclaimer

This application is intended for educational purposes only and does not provide medical advice.

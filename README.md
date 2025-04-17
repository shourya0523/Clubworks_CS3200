# 🎓 ClubWorks - Student Club Management System

<div align="center">
  <img src="https://img.shields.io/badge/Status-In%20Development-yellow" alt="Status: In Development">
  <img src="https://img.shields.io/badge/Course-CS%203200-blue" alt="Course: CS 3200">
  <img src="https://img.shields.io/badge/Spring-2025-green" alt="Spring 2025">
</div>

## 📋 Overview

ClubWorks is a comprehensive platform designed to streamline the management of student clubs and organizations at universities. The system connects students with clubs, helps club executives manage their organizations, and provides administrators and analysts with valuable insights.

> This project is built using a modern three-tier architecture with Streamlit, Flask, and MySQL.

## 🌟 Key Features

### 👨‍🎓 For Students
- Browse and discover clubs based on interests
- View upcoming events and applications
- Track club memberships and attendance
- Connect with other students through a social network
- Provide feedback on club experiences

### 👑 For Club Presidents
- Manage club membership and contact information
- Create and track events
- Monitor attendance statistics
- Receive anonymous feedback
- Submit funding and support requests

### 🔍 For Administrators
- Track student registrations and club profiles
- Monitor support requests
- View system-wide statistics
- Visualize the student-club engagement network
- Manage executive assignments

### 📊 For Analysts
- Analyze club performance metrics
- Track student engagement by major and graduation year
- Identify retention patterns
- Evaluate funding requests
- Generate insights on club interests and demographics

## 🛠️ Project Components

The project consists of three major components, each running in its own Docker container:

- **Streamlit App** (`./app` directory) - User interface
- **Flask REST API** (`./api` directory) - Business logic and data processing
- **MySQL Database** (`./database-files` directory) - Data storage

## 🚀 Getting Started

### Prerequisites

- A GitHub Account
- Git client (terminal-based or GUI like GitHub Desktop)
- VSCode with the Python Plugin
- Python distribution (Anaconda or Miniconda recommended)
- Docker Desktop

### Setting Up Your Personal Repo

1. In GitHub, click the **fork** button in the upper right corner of the repo screen.
2. When prompted, give the new repo a unique name, perhaps including your last name and the word 'personal'.
3. Once the fork has been created, clone YOUR forked version of the repo to your computer.
4. Set up the `.env` file in the `api` folder based on the `.env.template` file.
5. For running the testing containers (for your personal repo), use:
   ```bash
   # Start all containers in the background
   docker compose -f docker-compose-testing.yaml up -d
   
   # Shutdown and delete the containers
   docker compose -f docker-compose-testing.yaml down
   
   # Only start the database container
   docker compose -f docker-compose-testing.yaml up db -d
   
   # "Turn off" the containers but not delete them
   docker compose -f docker-compose-testing.yaml stop
   ```

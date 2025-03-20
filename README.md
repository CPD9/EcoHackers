# EcoHackers - Start Hack 2025

## Overview

Welcome to the **EcoHackers** GitHub repository for **Start Hack 2025**! Our aim is to create an innovative platform that leverages data-driven decision-making. 🧑🏻‍💻👩🏻‍💻👨🏽‍💻👩🏼‍💻

![giphy](https://github.com/user-attachments/assets/7690718c-8d58-4a2a-9b15-159f36c8df65)


## Tech Stack

We have chosen the following technologies for our implementation:

### **Backend (API & Data Management)**

- **Django (Python)** – For a robust and scalable backend, handling API requests, data processing, and database interactions.
- **Django REST Framework (DRF)** – To create a structured, efficient, and RESTful API.
- **PostgreSQL** – For managing structured environmental data efficiently.

### **Frontend (User Interface & Experience)**

- **React.js** – For building an interactive and dynamic user experience.
- **Tailwind CSS** – For modern, responsive, and easy-to-maintain styling.
- **Axios** – For seamless API communication between the frontend and backend.

### **Development & Collaboration Tools**

- **GitHub** – For version control and collaboration.
- **GitHub Actions** – For automated CI/CD processes.
- **VS Code** – Preferred code editor for development.
- **Docker** (Optional) – For containerized deployment.

## Purpose & Goal

The **EcoHackers** project aims to develop a **sustainability-focused web platform** that provides actionable insights using **AI and data analytics**. Our solution is designed to:

- Gather and analyze environmental data from multiple sources.
- Provide real-time sustainability recommendations.
- Enable seamless collaboration for eco-conscious communities and businesses.

## How to Get Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/EcoHackers/start-hack-2025.git
   git checkout -b 'create_your_branch'
   ```

2. **Navigate to the project directory:**
   ```bash
   cd EcoHackers
   ```
3. **Backend Setup:**

**Create a virtual environment:**
```bash
   python -m venv EcoHackers
   source EcoHackers/bin/activate  # On Windows use `EcoHackers\Scripts\activate`
   ```

**Install dependencies:**

```bash
pip install -r requirements.txt
   ```

**Run migrations:**

```bash
python manage.py migrate
   ```

**Start the Django development server:**
```bash
python manage.py runserver
   ```


4. **Frontend Setup:**
   
**Navigate to the frontend directory:**
```bash
cd frontend
   ```

**Install dependencies:**
```bash
npm install
```

**Start the React development server:**
```bash
npm start
```


# Branching Strategy

To maintain a structured workflow, we will use four main branches in this repository:
1. **API** - Handles the API-related development.
2. **Frontend** - Manages all front-end development and UI/UX design.
3. **Backend** - Covers backend-related tasks, including database interactions.
4. **Draft** - A general branch for testing and collaborative drafts.
   
**Working with Branches**

**Switching to a Branch**

```bash
git checkout <branch-name>
```

**Creating a New Branch**

```bash
git checkout -b <new-branch-name>
```

**Pulling the Latest Changes from a Branch**
```bash
git pull origin <branch-name>
```

**Pushing Changes to a Branch**

```bash
git add .
git commit -m "Your commit message"
git push origin <branch-name>
```

**Merging Changes from Another Branch**

```bash
git checkout <target-branch>
git merge <source-branch>
```

Deleting a Local Branch (After Merging)

```bash
git branch -d <branch-name>
```


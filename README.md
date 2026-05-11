# Task_Ticket_Manager

BeeHive is a full-stack task and sprint management system built for teams. It supports project management, sprint planning, kanban boards, task assignments, and employee management with role-based access control for admins and employees.

---

## Tech Stack

- **Backend:** FastAPI + SQLAlchemy (Python)
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript (no framework)
- **Auth:** JWT tokens + bcrypt

---

## Setting up the Python virtual environment

These instructions describe how to start your virtual environment inside the project.

### 1. Open a terminal in VS Code

- In VS Code, open this project folder.
- Open a terminal with **Ctrl+Shift+`** or by clicking **Terminal → New Terminal**.
- Make sure the terminal path is the project folder (VS Code usually does this automatically).

### 2. Create the virtual environment

Run:

```bash
python -m venv .venv
```

Then activate the virtual environment:

```bash
# Mac/Linux
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

After it's activated, you should see `(.venv)` before the folder path in your terminal.

### 3. Install dependencies

Run:

```bash
pip install -r requirements.txt
```

This installs all the packages needed for the project using the requirements file. It will likely be updated over the course of the project.

---

## Environment Variables

Create a `.env` file in the project root with the following:

```
DATABASE_URL=postgresql://user:password@localhost:5432/beehive
SECRET_KEY=your_long_random_secret_key
ALLOWED_ORIGINS=http://127.0.0.1:5500
```

---

## Running the Project

Start the backend:

```bash
uvicorn src.main:app --reload
```

Then open `HTML/index.html` using the VS Code Live Server extension. On first launch you will be redirected to setup to create an admin account.

---

## Working with Git branches

This guide shows how to create and switch between Git branches using the VS Code terminal or any terminal.

### 1. Creating a branch from the terminal

1. Open the integrated terminal in VS Code.
   - Menu: `View` → `Terminal`
   - Shortcut: <kbd>Ctrl</kbd> + <kbd>`</kbd> (backtick)

2. Make sure you are inside a Git repository:
   ```bash
   git status
   ```

3. Switch to the main branch and pull the latest changes:
   ```bash
   git checkout main
   git pull
   ```

4. Create a new branch and switch to it in one step:
   ```bash
   # Older syntax
   git checkout -b name-of-branch

   # Newer syntax
   git switch -c name-of-branch
   ```

5. Make your changes, then stage and commit:
   ```bash
   git add .
   git commit -m "Describe your changes here"
   ```

6. Push the new branch to GitHub:
   ```bash
   # Sets upstream tracking for the branch
   git push -u origin name-of-branch

   # Without setting upstream
   git push origin name-of-branch
   ```

### 2. Other useful branch commands

Create a branch without switching to it:
```bash
git branch name-of-branch
```

Switch to an existing branch:
```bash
git checkout name-of-branch
# or
git switch name-of-branch
```

List all local branches:
```bash
git branch
```

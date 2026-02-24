# Task_Ticket_Manager

This is a project where we will be making a Task Ticket Manager.

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
Then run the following command to activate the virtual enviornment
```bash
source .venv/bin/activate (Mac/Linux)
.\.venv\Scripts\Activate.ps1 (Windows Powershell)
```

After it's activated, it should show (.venv) before the folder path.
Then run: 
```bash
pip install -r requirements.txt
```
This will use the requirements text document to install the packages you will need for this project. It will be most likely updated over the course of the project. 


## Working with Git branches (VS Code & terminal)

This guide shows how to create and use Git branches in VS Code’s terminal, any terminal, and the VS Code UI.

---

## 1. Creating a Git branch from VS Code terminal

1. Open the integrated terminal in VS Code  
   - Menu: `View` → `Terminal`  
   - Shortcut: <kbd>Ctrl</kbd> + <kbd>`</kbd> (backtick)

2. Make sure you are in your project folder and inside a Git repository:
   ```bash
   git status
   ```
3. Switch to the source branch (usually main) and update it:
    ```bash
    git checkout main     # or: git switch main
    git pull
    ```
4. Create a new branch and switch to it in one step
    ```bash
    git checkout -b name-of-branch    # older syntax
    # or
    git switch -c name-of-branch      # newer syntax
    ```
5. Make your changes, then stage and commit:
    ```bash
    git add .
    git commit -m "Describe changes here"
    ```
6. Push the new branch to Github.
    ```bash
    git push -u origin name-of-branch     # sets upstream to the branch
    # or
    git push origin name-of-branch        # doesnt set upstream
    ```
## 2. Creating and Manually switching branches in any terminal 

1. Create a new branch without switching
     ```bash
     git branch name-of-branch
     ```
2. Switch to an existing branch
    ```bash
    git checkout name-of-branch
    # or
    git switch name-of-branch
    ```
3. List of all local branches
    ```bash
    git branch
    ```

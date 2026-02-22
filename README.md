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


### Expense Tracker (Simple Project)

This is a simple Expense Tracker made in Python. It lets you add expenses, see them, and save them in a JSON file.

### Features
- Add a new expense (amount, category, note, date)
- View all saved expenses
- Data saved in `expenses.json`
- Simple Python script and a small GUI

### How it works
- The program reads and writes expenses to `expenses.json`.
- Each expense has: `id`, `amount`, `category`, `note`, and `date`.
- You can run it from GUI window.

### How to run
- Run the GUI (easiest):
  - `run.py`


### Files
- `expense_tracker.py`: Main logic for handling expenses
- `expense_tracker_gui.py`: GUI to logic mapping 
- `expenses.json`: Stores the expenses data
- `run.py`: Small runner script

### Notes
- Make sure Python is installed.
- If `expenses.json` is missing, the program will create it the first time you save.

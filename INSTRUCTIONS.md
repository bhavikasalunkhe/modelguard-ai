# ModelGuard AI - Installation & Setup Instructions

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Running the Application](#running-the-application)
4. [First Run Checklist](#first-run-checklist)
5. [Troubleshooting](#troubleshooting)
6. [Using Sample Data](#using-sample-data)
7. [Development Setup](#development-setup)

---

## Prerequisites

Before installing ModelGuard AI, ensure you have:

### Required Software

#### Windows
1. **Python 3.9 or higher**
   - Download from: https://www.python.org/downloads/
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Verify: Open Command Prompt and type `python --version`

2. **Git** (optional, for version control)
   - Download from: https://git-scm.com/

#### Mac
```bash
# Install Python (if not already installed)
brew install python

# Verify
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3.9 python3-pip python3-venv
```

---

## Installation Steps

### Step 1: Extract the Project

1. Download the `modelguard-ai` folder
2. Extract it to a convenient location (e.g., `C:\Users\YourName\Documents\` on Windows)
3. Remember the folder path

### Step 2: Open Terminal/Command Prompt

**Windows:**
- Press `Win + R`
- Type `cmd`
- Press Enter

**Mac:**
- Press `Cmd + Space`
- Type `terminal`
- Press Enter

**Linux:**
- Press `Ctrl + Alt + T`

### Step 3: Navigate to Project Directory

```bash
# Windows example
cd C:\Users\YourName\Documents\modelguard-ai

# Mac/Linux example
cd ~/Documents/modelguard-ai

# Or just drag the folder into terminal (on Mac)
cd [drag modelguard-ai folder here]
```

**Verify you're in the right place:**
```bash
# You should see these files
dir          # Windows
ls -la       # Mac/Linux
```

You should see: `README.md`, `INSTRUCTIONS.md`, `requirements.txt`, `app/`, `src/`, etc.

### Step 4: Create Virtual Environment

A virtual environment isolates Python packages for this project.

**Windows:**
```bash
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

This creates a `venv` folder (may take 30-60 seconds).

### Step 5: Activate Virtual Environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```
*Note: If this fails with a permissions error, you may need to enable PowerShell script execution:*
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Success indicator:**
You should see `(venv)` at the start of your terminal line:
```
(venv) C:\Users\YourName\Documents\modelguard-ai>
```

### Step 6: Upgrade pip (Important)

```bash
python -m pip install --upgrade pip
```

This ensures you have the latest package installer.

### Step 7: Install Dependencies

```bash
pip install -r requirements.txt
```

**This will:**
- Download and install ~50 packages
- Take 5-15 minutes (depends on internet speed)
- Show `Successfully installed` when complete

**If you see any errors:**
- Note the package name
- See [Troubleshooting](#troubleshooting) section

### Step 8: Verify Installation

Test that everything installed correctly:

```bash
# Check Python packages
pip list

# Quick Python test
python -c "import pandas; import streamlit; import shap; print('✓ All packages installed!')"
```

---

## Running the Application

### Method 1: Streamlit Web Interface (Recommended)

**Step 1: Make sure virtual environment is active**
```bash
# You should see (venv) in your terminal
# If not, activate it:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

**Step 2: Start the Streamlit app**
```bash
streamlit run app/frontend/streamlit_app.py
```

**Step 3: Browser opens automatically**
- If not, open browser and go to: `http://localhost:8501`
- You should see the ModelGuard AI dashboard

**To stop the app:**
- Press `Ctrl + C` in the terminal

---

### Method 2: Using Visual Studio Code

**Step 1: Open the project**
- Open Visual Studio Code
- File → Open Folder
- Select the `modelguard-ai` folder
- Click "Select Folder"

**Step 2: Open Terminal in VS Code**
- View → Terminal (or press Ctrl + `)

**Step 3: Select Python interpreter**
- Bottom right corner, click "Select Python Interpreter"
- Choose the one in `./venv/bin/python` or `.\\venv\\Scripts\\python.exe`

**Step 4: Terminal automatically uses virtual environment**
```bash
streamlit run app/frontend/streamlit_app.py
```

**Step 5: Click the URL or open `http://localhost:8501`**

---

### Method 3: Using Python IDE

**PyCharm:**
1. File → Open → Select modelguard-ai folder
2. Configure interpreter: PyCharm → Preferences → Project → Python Interpreter
3. Click ⚙️ → Add → Existing Environment → Select `venv/bin/python`
4. Open Terminal: View → Tool Windows → Terminal
5. Run: `streamlit run app/frontend/streamlit_app.py`

**VS Code + Extensions:**
1. Install "Python" extension (Microsoft)
2. Install "Streamlit" extension (optional)
3. Open folder and select Python interpreter
4. Run the command above

---

## First Run Checklist

After installation, verify everything works:

- [ ] Virtual environment activated (see `(venv)` in terminal)
- [ ] All packages installed (`pip list` shows packages)
- [ ] Streamlit running (`streamlit run ...`)
- [ ] Browser opens to `http://localhost:8501`
- [ ] Dashboard loads with "Upload Dataset" section
- [ ] No red error messages

If any step fails, check [Troubleshooting](#troubleshooting).

---

## Using Sample Data

ModelGuard AI includes sample datasets. Here's how to use them:

### Sample 1: Clean Customer Churn Dataset

**File:** `data/sample/customer_churn.csv`

1. Open the Streamlit app
2. Click "📁 Upload Dataset"
3. Select `data/sample/customer_churn.csv`
4. **Target Column:** Type `churn`
5. Click "🔍 Analyze"

**Expected Results:**
- Data Quality Score: 82+
- Issues: 2-3 low severity
- Status: 🟢 LOW RISK

---

### Sample 2: Dataset with Issues

**File:** `data/sample/customer_churn_with_issues.csv`

1. Upload `data/sample/customer_churn_with_issues.csv`
2. **Target Column:** Type `churn`
3. Click "🔍 Analyze"

**Expected Results:**
- Data Quality Score: 45-55
- Issues: 5-7 including HIGH severity
- Detects: Imbalance, leakage, missing values
- Status: 🔴 HIGH RISK

---

### Sample 3: With Predictions

**Use Together:**
1. Upload `data/sample/customer_churn.csv`
2. Then upload `data/sample/churn_predictions.csv` (optional)
3. **Predictions Column:** Type `prediction`
4. See performance metrics appear

---

## Development Setup

If you want to modify the code or run tests:

### Run Tests

```bash
# Make sure virtual environment is active
pytest tests/ -v
```

**Expected output:**
```
test_data_quality.py::test_detect_duplicates PASSED
test_data_quality.py::test_detect_imbalance PASSED
test_leakage_detection.py::test_target_leakage PASSED
...
===================== 15 passed in 2.34s =====================
```

### Run Specific Test

```bash
pytest tests/test_data_quality.py -v
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

Then open `htmlcov/index.html` in browser.

### Modify Code in VS Code

1. Open any `.py` file
2. Edit as needed
3. Save (`Ctrl + S`)
4. Streamlit auto-reloads (you'll see "Rerun" button)
5. Click "Rerun" or it auto-runs

### Debug Mode

Add to any Python file:
```python
import pdb; pdb.set_trace()
```

Then run and the terminal becomes interactive debugger.

---

## Troubleshooting

### Problem: "Python command not found"

**Windows Solution:**
1. Uninstall Python
2. Reinstall from https://www.python.org/downloads/
3. **CHECK: "Add Python to PATH"** checkbox
4. Restart computer
5. Try again: `python --version`

**Mac/Linux Solution:**
```bash
# Use python3 instead
python3 --version
python3 -m venv venv
source venv/bin/activate
```

---

### Problem: "No module named 'streamlit'"

**Solution:**
```bash
# Make sure venv is activated (you see (venv) in terminal)
# If not:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall packages
pip install -r requirements.txt
```

---

### Problem: "ModuleNotFoundError: No module named 'src'"

**Solution:**
1. Make sure you're in the project root directory
2. Verify directory contains: `README.md`, `app/`, `src/`, etc.
3. Make sure Python interpreter is set correctly (in VS Code, select `./venv/bin/python`)
4. Restart the terminal and run again

---

### Problem: "Port 8501 is already in use"

**Solution 1 - Kill process using port:**
```bash
# Windows
netstat -ano | findstr :8501
taskkill /PID [PID number] /F

# Mac/Linux
lsof -ti:8501 | xargs kill -9
```

**Solution 2 - Use different port:**
```bash
streamlit run app/frontend/streamlit_app.py --server.port 8502
```

---

### Problem: "pip install" is very slow or fails

**Solution:**
```bash
# Use different pip index
pip install -i https://pypi.org/simple/ -r requirements.txt

# Or upgrade pip first
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

### Problem: "ImportError with SHAP"

**Solution:**
```bash
pip install --upgrade shap

# Or rebuild it
pip install --no-cache-dir shap
```

If still failing, may need C++ build tools (Visual Studio Build Tools on Windows).

---

### Problem: "Streamlit button not responding"

**Solution:**
1. Check browser console for errors (F12)
2. Refresh page (F5)
3. Stop Streamlit (Ctrl + C)
4. Start again: `streamlit run app/frontend/streamlit_app.py`

---

### Problem: "Virtual environment activation fails (PowerShell)"

**Windows PowerShell Solution:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try:
```bash
venv\Scripts\Activate.ps1
```

---

## Getting Help

### Check These First

1. **README.md** - Project overview and features
2. **tests/** - Example usage in test files
3. **data/sample/** - Example datasets
4. **app/frontend/streamlit_app.py** - Main application code

### Common Questions

**Q: Do I need to run setup every time?**
A: No, only when you first install. Next time, just activate venv and run streamlit.

**Q: Can I use Anaconda instead of venv?**
A: Yes, create conda environment: `conda create -n modelguard python=3.9`

**Q: How do I update packages?**
A: `pip install --upgrade -r requirements.txt`

**Q: Can I deploy this online?**
A: Yes, use Streamlit Cloud (free tier available): https://streamlit.io/cloud

---

## Quick Reference

### Essential Commands

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install/update packages
pip install -r requirements.txt

# Start application
streamlit run app/frontend/streamlit_app.py

# Run tests
pytest tests/ -v

# Deactivate virtual environment
deactivate
```

### Directory Navigation

```bash
# Windows
cd path\to\modelguard-ai

# Mac/Linux
cd ~/path/to/modelguard-ai

# Show current directory
pwd

# List files
ls -la  # Mac/Linux
dir     # Windows
```

---

## Next Steps

After successful installation:

1. **Explore Sample Data**
   - Try both sample datasets
   - See what the reports look like

2. **Use Your Own Data**
   - Prepare a CSV with a target column
   - Run analysis
   - Review the report

3. **Study the Code**
   - Open files in VS Code
   - Read the comments
   - Understand each module

4. **Run Tests**
   - `pytest tests/ -v`
   - See how the system validates itself

5. **Modify & Experiment**
   - Change thresholds in `configs/settings.py`
   - Add new checks
   - Build custom reports

---

## System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| Python | 3.9 | 3.10+ |
| RAM | 2GB | 4GB+ |
| Disk Space | 500MB | 1GB+ |
| OS | Windows 7+, macOS 10.12+, Ubuntu 16.04+ | Windows 10+, macOS 11+, Ubuntu 20.04+ |
| Internet | Only for installation | For LLM features |

---

## Performance Tips

1. **Use SSD** - Faster file operations
2. **Close unnecessary apps** - Frees up RAM for large datasets
3. **Use 64-bit Python** - Better performance than 32-bit
4. **Update packages regularly** - `pip install --upgrade -r requirements.txt`

---

**You're all set! Enjoy using ModelGuard AI! 🚀**

If you have questions, refer back to this guide or check the README.md file.

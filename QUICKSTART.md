# ModelGuard AI - Quick Start Guide

## ⚡ Get Running in 5 Minutes

### 1. Extract & Open Project (1 min)

```
1. Extract modelguard-ai.zip
2. Open Visual Studio Code
3. File → Open Folder → Select modelguard-ai
```

### 2. Setup Virtual Environment (1 min)

**Open Terminal in VS Code** (Ctrl + `)

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install Packages (2-3 min)

```bash
pip install -r requirements.txt
```

Wait for "Successfully installed" message.

### 4. Run the App (1 min)

```bash
streamlit run app/frontend/streamlit_app.py
```

**Browser opens automatically** at `http://localhost:8501`

---

## 🎯 First Analysis (2 minutes)

### Step 1: Upload Sample Data
1. Click "📁 Upload Dataset"
2. Navigate to: `data/sample/customer_churn_clean.csv`
3. Select it

### Step 2: Set Target Column
- In the right panel, select: `churn`

### Step 3: View Data
- Click "Tab 2" to see the data preview

### Step 4: Run Audit
1. Click "🔍 Analyze" tab
2. Click "▶️ Run Audit" button
3. Wait ~10 seconds for analysis

### Step 5: See Results
- Click "📊 Results" tab
- Scroll through the report

---

## 📊 Expected Results

For `customer_churn_clean.csv`:
- **Score**: 82+/100 ✅
- **Status**: 🟢 LOW RISK
- **Issues**: 2-3 low severity
- **Analysis time**: ~5 seconds

For `customer_churn_with_issues.csv`:
- **Score**: 45-55/100 ⚠️
- **Status**: 🔴 HIGH RISK
- **Issues**: 6-8 including leakage
- **Detected**: Class imbalance, missing values, suspicious features

---

## 💻 Code Usage (Optional)

### Use in Python Script

```python
import pandas as pd
from src.profiling.data_quality import DataQualityAuditor
from src.leakage.target_leakage import TargetLeakageDetector

# Load data
df = pd.read_csv('data/sample/customer_churn_clean.csv')
X = df.drop('churn', axis=1)
y = df['churn']

# Audit data quality
auditor = DataQualityAuditor(df, target_column='churn')
quality = auditor.audit()
print(f"Quality Score: {quality['quality_score']}")

# Detect leakage
detector = TargetLeakageDetector(X, y)
leakage = detector.detect()
print(f"Leakage Risk: {leakage['has_leakage']}")
```

### Run Tests

```bash
pytest tests/ -v
```

You should see:
```
test_data_quality.py::test_clean_data_passes PASSED
test_data_quality.py::test_duplicate_detection PASSED
...
===================== 6 passed in 2.34s =====================
```

---

## 📋 File Guide

| File | Purpose |
|------|---------|
| `app/frontend/streamlit_app.py` | **Start here** - Main web app |
| `src/profiling/data_quality.py` | Data quality checks |
| `src/leakage/target_leakage.py` | Leakage detection |
| `src/scoring/reliability_score.py` | Scoring engine |
| `data/sample/` | Example datasets |
| `requirements.txt` | Dependencies |

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
→ Check venv is activated (should see `(venv)` in terminal)

### "pip install" fails
→ Try: `pip install --upgrade pip` first

### "Port 8501 already in use"
→ Run: `streamlit run app/frontend/streamlit_app.py --server.port 8502`

### Streamlit not responding
→ Stop (Ctrl+C), restart: `streamlit run app/frontend/streamlit_app.py`

---

## 🎓 Learning Path

**5 min**: Run the app with sample data  
**15 min**: Review the `README.md` and `INSTRUCTIONS.md`  
**30 min**: Explore `src/profiling/data_quality.py` code  
**1 hour**: Read all comments in main modules  
**2 hours**: Run tests, modify thresholds in `configs/settings.py`

---

## 📤 Export Reports

After analysis:
1. Click "📊 Results" tab
2. Scroll to bottom
3. Click "📥 Export Report"
4. Choose: JSON or Text
5. File downloads automatically

---

## 🔗 Next Steps

1. **Try both sample datasets** - See how scoring differs
2. **Use your own data** - Upload CSV with features + target
3. **Read the code** - Start with `src/profiling/data_quality.py`
4. **Modify settings** - Edit `configs/settings.py` to tune thresholds
5. **Add custom checks** - Create new detection logic in appropriate modules

---

## ✨ Key Features to Try

✅ Upload CSV  
✅ Detect missing values  
✅ Find duplicate records  
✅ Identify class imbalance  
✅ Detect data leakage  
✅ Check validation strategy  
✅ Calculate reliability score  
✅ View recommendations  
✅ Download reports  

---

## 📞 Support

**Installation issues** → See `INSTRUCTIONS.md`  
**Feature questions** → Read `README.md`  
**Project structure** → Check `PROJECT_STRUCTURE.md`  
**Code questions** → Look at comments in `src/` files

---

## 🎉 You're All Set!

ModelGuard AI is ready to audit your ML models. 

**Start with**: `streamlit run app/frontend/streamlit_app.py`

Happy modeling! 🚀

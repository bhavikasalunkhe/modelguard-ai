# ModelGuard AI - ML Reliability & AI Review Platform

> An AI Second Opinion System for Machine Learning Models

ModelGuard AI is an intelligent ML auditing platform that analyzes datasets, notebooks, and model outputs to detect data leakage, validation errors, class imbalance, and methodological risks. It provides structured, evidence-based second opinions on model reliability.

## 🎯 What It Does

Upload a CSV dataset + model predictions, and ModelGuard AI generates:

✅ **Data Quality Report** — Missing values, duplicates, class imbalance  
✅ **Methodology Audit** — Train/test split, cross-validation checks  
✅ **Leakage Detection** — Target leakage, temporal leakage, preprocessing leakage  
✅ **Model Evaluation** — Classification metrics (Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC)  
✅ **SHAP Explanations** — Global and local feature importance  
✅ **Reliability Score** — Custom ModelGuard scoring (0-100)  
✅ **Risk Flags** — HIGH, MEDIUM, LOW severity issues  
✅ **Actionable Recommendations** — How to fix problems  

## 📊 Example Output

```
ModelGuard AI Report
====================

Overall Assessment: REVIEW REQUIRED
Reliability Score: 72/100

HIGH RISK (1 issue)
├─ Potential Target Leakage: feature 'final_score'
│  Confidence: 91%

MEDIUM RISK (2 issues)
├─ Class Imbalance: Minority class 3.2%
├─ Validation Problem: Random split with temporal data

Model Performance
├─ Accuracy: 94.2%
├─ Recall: 41.7% ⚠️  (Model misses 58% of positive cases)
├─ F1: 0.58
├─ PR-AUC: 0.67
└─ ROC-AUC: 0.82

Top Risk Drivers
1. Leakage Risk: 25/100
2. Validation Issues: 18/100
3. Class Imbalance: 12/100

Recommendations
1. Remove suspected leakage feature
2. Implement time-based validation
3. Use stratified cross-validation
4. Optimize for PR-AUC instead of accuracy
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Visual Studio Code (or any IDE)
- 2GB free disk space

### Installation (5 minutes)

```bash
# 1. Navigate to project directory
cd modelguard-ai

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
streamlit run app/frontend/streamlit_app.py
```

**That's it!** The app opens at `http://localhost:8501`

---

## 📁 Project Structure

```
modelguard-ai/
│
├── 📄 README.md                 (This file)
├── 📄 INSTRUCTIONS.md           (Detailed setup guide)
├── 📄 requirements.txt           (Python dependencies)
│
├── app/
│   ├── frontend/
│   │   └── streamlit_app.py     (Main web interface)
│   └── api/
│       └── main.py              (FastAPI backend - optional)
│
├── src/
│   ├── __init__.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── dataset_loader.py    (Load CSV, Excel, JSON)
│   │
│   ├── profiling/
│   │   ├── __init__.py
│   │   ├── data_quality.py      (Missing values, duplicates, imbalance)
│   │   ├── target_analysis.py   (Target distribution analysis)
│   │   └── feature_analysis.py  (Feature statistics & types)
│   │
│   ├── leakage/
│   │   ├── __init__.py
│   │   ├── target_leakage.py    (Suspicious features)
│   │   ├── temporal_leakage.py  (Time-based issues)
│   │   └── preprocessing_leakage.py (Fit before split)
│   │
│   ├── validation/
│   │   ├── __init__.py
│   │   ├── split_checker.py     (Train/test split analysis)
│   │   ├── cross_validation.py  (CV detection)
│   │   └── preprocessing_checker.py (Pipeline checks)
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── classification.py    (Classification metrics)
│   │   ├── regression.py        (Regression metrics)
│   │   └── calibration.py       (Probability calibration)
│   │
│   ├── explainability/
│   │   ├── __init__.py
│   │   └── shap_analysis.py     (SHAP explanations)
│   │
│   ├── scoring/
│   │   ├── __init__.py
│   │   └── reliability_score.py (ModelGuard Reliability Score)
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── reviewer.py          (LLM-based second opinion)
│   │   └── prompts.py           (LLM prompts)
│   │
│   ├── reporting/
│   │   ├── __init__.py
│   │   └── report_generator.py  (Generate final report)
│   │
│   └── utils.py                 (Helper functions)
│
├── tests/
│   ├── __init__.py
│   ├── test_data_quality.py
│   ├── test_leakage_detection.py
│   ├── test_evaluation.py
│   └── test_integration.py
│
├── data/
│   ├── sample/
│   │   ├── customer_churn.csv              (Clean sample)
│   │   ├── customer_churn_with_issues.csv (Bad sample)
│   │   ├── churn_predictions.csv          (Predictions)
│   │   └── README.md
│   └── synthetic/
│       └── generate_test_data.py
│
├── configs/
│   └── settings.py              (Configuration)
│
├── notebooks/
│   └── example_analysis.ipynb   (Jupyter example)
│
└── reports/
    └── (Generated reports saved here)
```

---

## 📖 How to Use

### Step 1: Prepare Your Data

You need:
- **CSV file** with your dataset
- **Target column name** (e.g., "churn", "prediction", "target")
- **Model predictions** (optional but recommended)

Example CSV format:
```
age,income,customer_lifetime_value,previous_month_revenue,final_score,churn
25,35000,5000,1200,0.92,1
30,45000,8000,1500,0.87,0
35,55000,12000,2000,0.95,1
```

### Step 2: Launch the App

```bash
streamlit run app/frontend/streamlit_app.py
```

### Step 3: Upload Dataset

1. Open web browser to `http://localhost:8501`
2. Click "📁 Upload Dataset"
3. Select your CSV file
4. Specify the target column
5. (Optional) Upload model predictions

### Step 4: Review Results

ModelGuard AI automatically generates:
- Data quality checks
- Leakage detection
- Validation methodology analysis
- Performance metrics
- Feature importance (SHAP)
- Reliability score
- AI second opinion

### Step 5: Export Report

Click "📥 Download Report" to save as PDF/JSON

---

## 🔍 Core Features

### 1. Data Quality Auditor
Detects:
- Missing values (%)
- Duplicate records
- Constant columns
- High-cardinality features
- Class imbalance
- Outliers (IQR method)
- Data type mismatches

### 2. ML Methodology Auditor
Checks:
- Train/test split approach
- Cross-validation strategy
- Preprocessing timing (before/after split)
- Pipeline implementation
- Hyperparameter tuning

### 3. Data Leakage Detector
Identifies:
- Target leakage (high correlations)
- Temporal leakage (future information)
- Preprocessing leakage (fit on all data)
- Duplicate record leakage
- Suspicious feature names

### 4. Model Performance Auditor
Calculates:
- **Classification**: Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC, Log Loss, Brier Score
- **Regression**: MAE, RMSE, R², MAPE
- Confusion matrices
- Residual analysis

### 5. SHAP Explainability
Shows:
- Global feature importance
- Local prediction explanations
- Feature dependence plots
- SHAP force plots

### 6. Reliability Scoring
Components (100 total):
- Data Quality: 20 points
- Validation: 20 points
- Leakage Risk: 20 points
- Model Performance: 20 points
- Explainability: 10 points
- Reproducibility: 10 points

Status:
- 80-100: 🟢 LOW RISK
- 60-79: 🟠 REVIEW REQUIRED
- 0-59: 🔴 HIGH RISK

---

## 🧪 Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test:
```bash
pytest tests/test_data_quality.py -v
```

Run with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

---

## 💻 Example Usage (Python)

```python
from src.ingestion.dataset_loader import DatasetLoader
from src.profiling.data_quality import DataQualityAuditor
from src.evaluation.classification import ClassificationEvaluator
from src.reporting.report_generator import ReportGenerator

# Load data
X, y = DatasetLoader.load_with_target('data/customer_churn.csv', 'churn')

# Audit data quality
quality_auditor = DataQualityAuditor(X.copy(), target=y)
quality_report = quality_auditor.audit()

# Load predictions
predictions = DatasetLoader.load_dataset('data/predictions.csv')['prediction']

# Evaluate model
evaluator = ClassificationEvaluator(y, predictions)
perf_report = evaluator.evaluate()

# Generate full report
generator = ReportGenerator()
full_report = generator.generate(
    data_quality=quality_report,
    performance=perf_report,
    predictions=predictions,
    target=y
)

# Save report
generator.save_report(full_report, 'reports/model_assessment.json')
```

---

## 🔧 Configuration

Edit `configs/settings.py` to customize:
- Missing value thresholds
- Outlier detection sensitivity
- Imbalance detection thresholds
- LLM model selection
- Report format

---

## 📦 Dependencies

All packages are in `requirements.txt`:
- pandas, numpy, scipy
- scikit-learn, xgboost
- shap (SHAP explanations)
- streamlit (web UI)
- fastapi, uvicorn (API backend)
- mlflow (experiment tracking)
- plotly, matplotlib, seaborn (visualization)

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'src'"
**Solution**: Make sure virtual environment is activated
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### "Streamlit: command not found"
**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt
```

### "Port 8501 already in use"
**Solution**: Run on different port
```bash
streamlit run app/frontend/streamlit_app.py --server.port 8502
```

### "SHAP import error"
**Solution**: Reinstall SHAP with build tools
```bash
pip install --upgrade shap
```

---

## 📚 Sample Datasets

Three sample datasets included:

1. **customer_churn.csv** (Good model)
   - Clean data
   - Proper validation
   - Expected score: 80+

2. **customer_churn_with_issues.csv** (Problematic)
   - Class imbalance (7% minority)
   - Leakage candidates
   - Missing values
   - Expected score: 45-55

3. **churn_predictions.csv** (Predictions)
   - Pre-computed predictions
   - Use with above for evaluation

---

## 🎓 Learning Resources

The project demonstrates:
- Data quality assessment
- ML methodology validation
- Data leakage detection
- Model evaluation best practices
- SHAP explanations
- LLM integration for report generation
- Streamlit dashboard development
- Professional Python project structure

---

## 📈 Next Steps / Roadmap

**Phase 1** (Current): Basic ML audit ✅
**Phase 2**: Advanced methodology checks
**Phase 3**: Notebook/script analysis (AST)
**Phase 4**: Model comparison system
**Phase 5**: Production drift detection
**Phase 6**: Custom thresholds & rules
**Phase 7**: Team collaboration features

---

## 🤝 Contributing

This is an open-source project. Feel free to:
- Add new detection rules
- Improve SHAP integration
- Add support for more file formats
- Enhance the UI/UX
- Add regression model checks
- Implement drift detection

---

## 📝 License

MIT License - Feel free to use for educational and commercial purposes

---

## 📞 Support

For issues or questions:
1. Check INSTRUCTIONS.md for detailed setup
2. Review test cases in `tests/`
3. Check sample data in `data/sample/`

---

## ⭐ Citation

If you use ModelGuard AI in your work, cite as:

```
ModelGuard AI - ML Reliability & AI Review Platform
An intelligent auditing system for machine learning model assessment
```

---

**Happy modeling! 🚀**

*Built for Data Scientists who want reliable ML models*

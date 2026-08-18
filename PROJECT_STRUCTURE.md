# ModelGuard AI - Project Structure

## 📁 Complete File Organization

```
modelguard-ai/
│
├── 📄 README.md                           (Project overview & features)
├── 📄 INSTRUCTIONS.md                     (Setup & installation guide)
├── 📄 PROJECT_STRUCTURE.md                (This file)
├── 📄 requirements.txt                    (Python dependencies)
├── 📄 .gitignore                          (Git ignore rules)
│
├── 📂 app/                                (Web application)
│   ├── frontend/
│   │   └── streamlit_app.py               (Main web UI - 700+ lines)
│   └── api/                               (Optional FastAPI backend)
│
├── 📂 src/                                (Core logic - 3000+ lines)
│   │
│   ├── __init__.py
│   │
│   ├── 📂 ingestion/                      (Data loading)
│   │   ├── __init__.py
│   │   └── dataset_loader.py              (CSV, Excel, JSON, Parquet loader)
│   │
│   ├── 📂 profiling/                      (Data analysis)
│   │   ├── __init__.py
│   │   ├── data_quality.py                (Quality audit - missing values, duplicates, imbalance)
│   │   ├── target_analysis.py             (Target variable analysis)
│   │   └── feature_analysis.py            (Feature statistics)
│   │
│   ├── 📂 leakage/                        (Leakage detection)
│   │   ├── __init__.py
│   │   ├── target_leakage.py              (High correlations, suspicious names)
│   │   ├── temporal_leakage.py            (Time-based leakage)
│   │   └── preprocessing_leakage.py       (Fit before split issues)
│   │
│   ├── 📂 validation/                     (Validation strategy checks)
│   │   ├── __init__.py
│   │   ├── split_checker.py               (Train/test split analysis)
│   │   ├── cross_validation.py            (CV recommendations)
│   │   └── preprocessing_checker.py       (Pipeline best practices)
│   │
│   ├── 📂 evaluation/                     (Model performance metrics)
│   │   ├── __init__.py
│   │   ├── classification.py              (Classification metrics: Accuracy, F1, ROC-AUC, PR-AUC)
│   │   ├── regression.py                  (Regression metrics: MAE, RMSE, R²)
│   │   └── calibration.py                 (Probability calibration check)
│   │
│   ├── 📂 explainability/                 (Model explanations)
│   │   ├── __init__.py
│   │   └── shap_analysis.py               (SHAP-based feature importance)
│   │
│   ├── 📂 scoring/                        (Reliability scoring)
│   │   ├── __init__.py
│   │   └── reliability_score.py           (Custom ModelGuard score: 0-100)
│   │
│   ├── 📂 reporting/                      (Report generation)
│   │   ├── __init__.py
│   │   └── report_generator.py            (JSON, text, display formatting)
│   │
│   └── 📂 drift/                          (Phase 2: Production drift detection)
│       └── __init__.py
│
├── 📂 tests/                              (Unit tests - 200+ lines)
│   ├── __init__.py
│   ├── test_data_quality.py               (Data quality tests)
│   └── test_*.py                          (Additional tests)
│
├── 📂 data/                               (Datasets)
│   ├── sample/
│   │   ├── customer_churn_clean.csv       (Good data example)
│   │   └── customer_churn_with_issues.csv (Problematic data example)
│   └── synthetic/
│
├── 📂 configs/                            (Configuration)
│   └── settings.py                        (Thresholds & parameters)
│
├── 📂 notebooks/                          (Jupyter notebooks)
│   └── (Example notebooks can be added)
│
└── 📂 models/                             (Trained models - if using ML)
    └── (Model artifacts can be saved here)
```

## 📊 Module Breakdown

### Ingestion (Dataset Loading)
- **dataset_loader.py** (250+ lines)
  - Load CSV, Excel, JSON, Parquet
  - Handle file upload from web
  - Validate data structure
  - Infer data types

### Profiling (Data Analysis)  
- **data_quality.py** (400+ lines)
  - Detect missing values
  - Find duplicates
  - Identify constant columns
  - Detect class imbalance
  - Find outliers (IQR method)
  - Check data types
  - Calculate quality score

- **target_analysis.py** (150+ lines)
  - Classify vs Regression
  - Distribution analysis
  - Class balance assessment
  - Target statistics

- **feature_analysis.py** (150+ lines)
  - Numeric feature stats
  - Categorical feature stats
  - Missing patterns
  - Cardinality analysis

### Leakage Detection (Data Leakage)
- **target_leakage.py** (250+ lines)
  - Suspicious feature names
  - High correlations
  - Information content analysis

- **temporal_leakage.py** (200+ lines)
  - Temporal feature detection
  - Ordering checks
  - Post-event feature detection

- **preprocessing_leakage.py** (200+ lines)
  - Scaled features detection
  - Imputation signs
  - Encoding detection

### Validation (Strategy Checks)
- **split_checker.py** (150+ lines)
  - Train/test split strategy
  - Temporal data detection
  - Class stratification check

- **cross_validation.py** (50+ lines)
  - CV recommendations
  - Best practices

- **preprocessing_checker.py** (100+ lines)
  - Pipeline recommendations
  - Common mistakes

### Evaluation (Performance Metrics)
- **classification.py** (250+ lines)
  - Accuracy, Precision, Recall, F1
  - ROC-AUC, PR-AUC
  - Confusion matrix
  - Log loss, Brier score

- **regression.py** (150+ lines)
  - MAE, RMSE, R²
  - MAPE
  - Residual analysis

- **calibration.py** (100+ lines)
  - Probability calibration
  - Expected Calibration Error

### Explainability (Model Interpretation)
- **shap_analysis.py** (100+ lines)
  - Feature importance
  - Feature effects
  - Prediction explanations

### Scoring (Reliability Assessment)
- **reliability_score.py** (300+ lines)
  - Data Quality: 20 pts
  - Validation: 20 pts
  - Leakage Risk: 20 pts
  - Performance: 20 pts
  - Explainability: 10 pts
  - Reproducibility: 10 pts
  - **Total: 100 pts**
  - Status: LOW RISK (80+), REVIEW (60-79), HIGH RISK (<60)

### Reporting (Report Generation)
- **report_generator.py** (250+ lines)
  - Executive summary
  - JSON export
  - Text export
  - Terminal display

### Frontend (Web Interface)
- **streamlit_app.py** (700+ lines)
  - Data upload
  - Interactive analysis
  - Results visualization
  - Report download

## 📈 Code Statistics

| Component | Lines | Purpose |
|-----------|-------|---------|
| Core Modules | 3000+ | Main analysis logic |
| Streamlit App | 700+ | Web interface |
| Tests | 200+ | Unit testing |
| Configuration | 100+ | Settings & parameters |
| **Total** | **~4000+** | **Complete system** |

## 🔄 Data Flow

```
User Upload (CSV)
    ↓
Dataset Loader (validate & parse)
    ↓
Data Quality Audit (20 checks)
    ↓
Target Analysis
    ↓
Feature Analysis
    ↓
Leakage Detection (3 types)
    ↓
Validation Checks
    ↓
Performance Evaluation
    ↓
Reliability Scoring
    ↓
Report Generation
    ↓
Display & Download
```

## 🛠️ Core Technologies

- **Python 3.9+**: Core language
- **Pandas/NumPy**: Data processing
- **Scikit-learn**: ML utilities
- **XGBoost**: Gradient boosting
- **SHAP**: Explainability
- **Streamlit**: Web UI
- **Plotly**: Interactive charts
- **Pytest**: Testing

## 📦 Key Classes & Functions

### Main Audit Workflow
```python
# 1. Load data
from src.ingestion.dataset_loader import DatasetLoader
X, y = DatasetLoader.load_with_target('data.csv', 'target')

# 2. Audit data quality
from src.profiling.data_quality import DataQualityAuditor
auditor = DataQualityAuditor(df, target_column='target')
quality_results = auditor.audit()

# 3. Detect leakage
from src.leakage.target_leakage import TargetLeakageDetector
detector = TargetLeakageDetector(X, y)
leakage_results = detector.detect()

# 4. Evaluate performance
from src.evaluation.classification import ClassificationEvaluator
evaluator = ClassificationEvaluator(y_true, y_pred)
perf_results = evaluator.evaluate()

# 5. Calculate score
from src.scoring.reliability_score import ReliabilityScorer
scorer = ReliabilityScorer()
score = scorer.calculate(all_results)

# 6. Generate report
from src.reporting.report_generator import ReportGenerator
generator = ReportGenerator()
report = generator.generate(all_results)
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_data_quality.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## 🚀 Deployment Ready

- ✅ Modular design (easy to extend)
- ✅ Comprehensive error handling
- ✅ Well-documented code
- ✅ Configurable thresholds
- ✅ Professional structure
- ✅ Unit tests included
- ✅ Sample data provided
- ✅ Interactive web UI
- ✅ Export functionality
- ✅ Production-grade code

## 📝 Next Steps

1. **Run the app**: `streamlit run app/frontend/streamlit_app.py`
2. **Try sample data**: Upload `data/sample/customer_churn_clean.csv`
3. **Review code**: Start with `src/profiling/data_quality.py`
4. **Run tests**: `pytest tests/ -v`
5. **Extend features**: Add new checks in respective modules

## 🎓 Learning Path

1. Start: Data Quality Auditor
2. Then: Leakage Detection
3. Then: Evaluation Metrics
4. Then: Reliability Scoring
5. Finally: Full integration in Streamlit

Each module is self-contained and can be used independently!

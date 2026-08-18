"""
Configuration settings for ModelGuard AI
"""

# Data Quality Thresholds
DATA_QUALITY_THRESHOLDS = {
    'missing_values_high': 50,      # % - HIGH severity
    'missing_values_medium': 20,    # % - MEDIUM severity
    'duplicate_threshold_high': 5,  # % - HIGH severity
    'duplicate_threshold_medium': 1, # % - MEDIUM severity
    'imbalance_threshold_high': 5,  # % - HIGH severity (minority class)
    'imbalance_threshold_medium': 20, # % - MEDIUM severity
    'outlier_threshold': 5,         # % - threshold for outlier detection
    'cardinality_threshold': 100,   # unique values threshold for high cardinality
}

# Leakage Detection Thresholds
LEAKAGE_THRESHOLDS = {
    'correlation_high': 0.8,        # Correlation threshold for high risk
    'correlation_medium': 0.6,      # Correlation threshold for medium risk
    'name_confidence': 0.7,         # Confidence for suspicious names
}

# Validation Thresholds
VALIDATION_THRESHOLDS = {
    'min_test_size': 0.1,           # Minimum test set size (10%)
    'min_cv_folds': 3,              # Minimum cross-validation folds
}

# Scoring Thresholds
SCORING_THRESHOLDS = {
    'low_risk_min': 80,             # Score for low risk (80-100)
    'review_required_min': 60,      # Score for review required (60-79)
    'high_risk_max': 59,            # Score for high risk (0-59)
}

# Model Performance Thresholds
PERFORMANCE_THRESHOLDS = {
    'accuracy_good': 0.80,
    'recall_good': 0.80,
    'precision_good': 0.80,
    'f1_good': 0.75,
    'auc_good': 0.75,
}

# Leakage Keywords
LEAKAGE_KEYWORDS = [
    'target', 'outcome', 'result', 'label',
    'final_score', 'final', 'actual', 'true',
    'prediction', 'pred', 'forecast',
    'y_', 'answer', 'ground_truth',
    'payment_status', 'churn_date', 'cancellation',
    'post_', 'after_', 'during_', 'future_',
    'approved', 'rejected', 'declined',
]

# Feature Analysis Settings
FEATURE_ANALYSIS_SETTINGS = {
    'max_unique_numeric': 100,      # Threshold for treating numeric as categorical
    'high_cardinality_pct': 50,     # % cardinality threshold
}

# Report Settings
REPORT_SETTINGS = {
    'max_issues_in_report': 20,
    'max_recommendations': 10,
    'include_timestamps': True,
    'formats': ['json', 'html', 'pdf'],  # Supported export formats
}

# Performance Settings
PERFORMANCE_SETTINGS = {
    'use_gpu': False,               # Use GPU for computations
    'n_jobs': -1,                   # Number of parallel jobs (-1 = all)
    'sample_size': None,            # Subsample for large datasets (None = no subsample)
}

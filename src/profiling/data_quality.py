"""
Data Quality Auditor Module

Detects issues in raw datasets before modeling:
- Missing values
- Duplicate records
- Constant columns
- Class imbalance
- Outliers
- Data type inconsistencies
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict


@dataclass
class DataQualityIssue:
    """Represents a single data quality issue."""
    check_name: str
    severity: str  # HIGH, MEDIUM, LOW
    column: str
    message: str
    evidence: str
    recommendation: str
    
    def to_dict(self):
        return asdict(self)


class DataQualityAuditor:
    """
    Audit dataset quality and detect data issues.
    
    Checks:
    - Missing values
    - Duplicate rows
    - Constant/near-constant columns
    - Class imbalance
    - Outliers
    - Data type issues
    - High cardinality
    """
    
    def __init__(self, df: pd.DataFrame, target_column: str = None):
        """
        Initialize auditor.
        
        Args:
            df: DataFrame to audit
            target_column: Name of target column (for imbalance detection)
        """
        self.df = df
        self.target_column = target_column
        self.issues: List[DataQualityIssue] = []
    
    def audit(self) -> Dict:
        """
        Run all quality checks.
        
        Returns:
            Dictionary with audit results
        """
        self.check_missing_values()
        self.check_duplicates()
        self.check_constant_columns()
        self.check_near_constant_columns()
        self.check_target_imbalance()
        self.check_outliers()
        self.check_data_types()
        self.check_high_cardinality()
        
        return self.get_report()
    
    def check_missing_values(self):
        """Detect missing values."""
        missing_pct = (self.df.isnull().sum() / len(self.df) * 100).sort_values(ascending=False)
        
        for col, pct in missing_pct[missing_pct > 0].items():
            if pct > 50:
                severity = "HIGH"
            elif pct > 20:
                severity = "MEDIUM"
            else:
                severity = "LOW"
            
            self.issues.append(DataQualityIssue(
                check_name="Missing Values",
                severity=severity,
                column=col,
                message=f"{pct:.1f}% missing values",
                evidence=f"Count: {self.df[col].isnull().sum()} / {len(self.df)} rows",
                recommendation="Investigate cause; impute, remove, or handle separately"
            ))
    
    def check_duplicates(self):
        """Detect duplicate rows."""
        num_duplicates = self.df.duplicated().sum()
        
        if num_duplicates > 0:
            pct_duplicate = (num_duplicates / len(self.df) * 100)
            
            severity = "MEDIUM" if pct_duplicate <= 5 else "HIGH"
            
            self.issues.append(DataQualityIssue(
                check_name="Duplicate Records",
                severity=severity,
                column="entire_dataset",
                message=f"{num_duplicates} duplicate rows detected",
                evidence=f"{pct_duplicate:.2f}% of dataset ({num_duplicates}/{len(self.df)} rows)",
                recommendation="Remove duplicates before modeling; use df.drop_duplicates()"
            ))
    
    def check_constant_columns(self):
        """Detect columns with no variation."""
        for col in self.df.columns:
            if self.df[col].nunique() == 1:
                self.issues.append(DataQualityIssue(
                    check_name="Constant Column",
                    severity="HIGH",
                    column=col,
                    message="Column has only one unique value",
                    evidence=f"Unique values: 1 (value: {self.df[col].iloc[0]})",
                    recommendation="Remove before modeling; provides no information"
                ))
    
    def check_near_constant_columns(self):
        """Detect columns with nearly no variation."""
        for col in self.df.columns:
            if self.df[col].dtype in ['object', 'category']:
                continue
            
            # Calculate variation
            value_counts = self.df[col].value_counts()
            if len(value_counts) > 1:
                most_common_pct = value_counts.iloc[0] / len(self.df) * 100
                
                if most_common_pct > 99:
                    self.issues.append(DataQualityIssue(
                        check_name="Near-Constant Column",
                        severity="MEDIUM",
                        column=col,
                        message=f"{most_common_pct:.1f}% of values are the same",
                        evidence=f"Most common value appears {most_common_pct:.1f}% of time",
                        recommendation="Consider removing; limited predictive value"
                    ))
    
    def check_target_imbalance(self):
        """Detect class imbalance in target."""
        if self.target_column and self.target_column in self.df.columns:
            target = self.df[self.target_column]
            
            # Check if classification (categorical or binary numeric)
            if target.dtype in ['object', 'category'] or target.nunique() < 20:
                value_counts = target.value_counts(normalize=True).sort_values()
                min_class_pct = value_counts.iloc[0] * 100
                max_class_pct = value_counts.iloc[-1] * 100
                
                if min_class_pct < 5:
                    severity = "HIGH"
                elif min_class_pct < 20:
                    severity = "MEDIUM"
                else:
                    severity = "LOW"
                    return  # Don't report if well-balanced
                
                dist_str = "\n".join([f"  {k}: {v*100:.1f}%" for k, v in value_counts.items()])
                
                self.issues.append(DataQualityIssue(
                    check_name="Class Imbalance",
                    severity=severity,
                    column=self.target_column,
                    message=f"Minority class: {min_class_pct:.1f}%",
                    evidence=f"Class distribution:\n{dist_str}",
                    recommendation="Use stratified split, class weights, or F1/PR-AUC metrics"
                ))
    
    def check_outliers(self):
        """Detect potential outliers using IQR method."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            if IQR == 0:
                continue
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
            outlier_pct = (len(outliers) / len(self.df) * 100)
            
            if outlier_pct > 5:
                self.issues.append(DataQualityIssue(
                    check_name="Outliers Detected",
                    severity="LOW",
                    column=col,
                    message=f"{outlier_pct:.2f}% potential outliers",
                    evidence=f"Count: {len(outliers)} rows; Range: [{self.df[col].min():.2f}, {self.df[col].max():.2f}]",
                    recommendation="Investigate; may be legitimate or data errors; consider robust scaling"
                ))
    
    def check_data_types(self):
        """Check for inconsistent or suspicious data types."""
        for col in self.df.columns:
            # Check if object type contains mostly numeric-looking values
            if self.df[col].dtype == 'object':
                sample = self.df[col].dropna().astype(str).head(100)
                numeric_looking = sample.str.match(r'^-?\d+\.?\d*$').sum()
                
                if len(sample) > 0 and numeric_looking / len(sample) > 0.8:
                    self.issues.append(DataQualityIssue(
                        check_name="Data Type Mismatch",
                        severity="MEDIUM",
                        column=col,
                        message=f"Column stored as text but contains numeric values",
                        evidence=f"{numeric_looking}/{len(sample)} sample values look numeric",
                        recommendation=f"Convert to numeric: pd.to_numeric({col})"
                    ))
    
    def check_high_cardinality(self):
        """Detect high-cardinality categorical features."""
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        
        for col in categorical_cols:
            n_unique = self.df[col].nunique()
            cardinality_ratio = n_unique / len(self.df)
            
            if n_unique > 100 and cardinality_ratio > 0.5:
                self.issues.append(DataQualityIssue(
                    check_name="High Cardinality",
                    severity="MEDIUM",
                    column=col,
                    message=f"{n_unique} unique values ({cardinality_ratio*100:.1f}% cardinality)",
                    evidence=f"Unique values: {n_unique}; Cardinality ratio: {cardinality_ratio:.3f}",
                    recommendation="Consider encoding, grouping, or one-hot encoding with care"
                ))
    
    def get_report(self) -> Dict:
        """
        Generate audit report.
        
        Returns:
            Dictionary containing audit results
        """
        if not self.issues:
            quality_score = 100
        else:
            high = sum(1 for i in self.issues if i.severity == "HIGH")
            medium = sum(1 for i in self.issues if i.severity == "MEDIUM")
            low = sum(1 for i in self.issues if i.severity == "LOW")
            
            quality_score = max(0, 100 - (high * 15 + medium * 5 + low * 2))
        
        # Determine status
        if quality_score >= 80:
            status = "✓ Good Quality"
            status_icon = "🟢"
        elif quality_score >= 60:
            status = "⚠ Needs Review"
            status_icon = "🟠"
        else:
            status = "✗ High Risk"
            status_icon = "🔴"
        
        return {
            'quality_score': quality_score,
            'status': status,
            'status_icon': status_icon,
            'total_issues': len(self.issues),
            'high_severity': sum(1 for i in self.issues if i.severity == "HIGH"),
            'medium_severity': sum(1 for i in self.issues if i.severity == "MEDIUM"),
            'low_severity': sum(1 for i in self.issues if i.severity == "LOW"),
            'issues': [i.to_dict() for i in self.issues]
        }

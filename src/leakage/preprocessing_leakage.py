"""
Preprocessing Leakage Detector

Detects when preprocessing operations (scaling, imputation, encoding)
are applied before train/test split, causing information leakage.
"""

import pandas as pd
import numpy as np
from typing import Dict, List


class PreprocessingLeakageDetector:
    """Detect preprocessing leakage."""
    
    def __init__(self, X: pd.DataFrame, y: pd.Series = None):
        """
        Initialize detector.
        
        Args:
            X: Features DataFrame
            y: Target series (optional)
        """
        self.X = X
        self.y = y
        self.issues = []
    
    def detect(self) -> Dict:
        """
        Detect preprocessing leakage issues.
        
        Returns:
            Dictionary with detection results
        """
        self._check_scaled_features()
        self._check_imputed_features()
        self._check_encoded_features()
        
        return self.get_report()
    
    def _check_scaled_features(self):
        """Check if features appear to be scaled."""
        numeric_cols = self.X.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            col_data = self.X[col].dropna()
            
            if len(col_data) == 0:
                continue
            
            # Check if mean is ~0 and std is ~1 (StandardScaler)
            mean = col_data.mean()
            std = col_data.std()
            
            if abs(mean) < 0.1 and abs(std - 1.0) < 0.1:
                self.issues.append({
                    'type': 'likely_scaled',
                    'feature': col,
                    'severity': 'MEDIUM',
                    'message': f"Feature appears to be StandardScaled (mean≈{mean:.3f}, std≈{std:.3f})",
                    'evidence': f"Mean: {mean:.4f}, Std: {std:.4f}",
                    'risk': 'If scaler was fit on entire dataset, this is leakage',
                    'recommendation': 'Fit scaler on training data only; use sklearn Pipeline'
                })
            
            # Check if min~0 and max~1 (MinMaxScaler)
            min_val = col_data.min()
            max_val = col_data.max()
            
            if abs(min_val) < 0.01 and abs(max_val - 1.0) < 0.01:
                self.issues.append({
                    'type': 'likely_minmax_scaled',
                    'feature': col,
                    'severity': 'MEDIUM',
                    'message': f"Feature appears to be MinMaxScaled (min≈{min_val:.3f}, max≈{max_val:.3f})",
                    'evidence': f"Min: {min_val:.4f}, Max: {max_val:.4f}",
                    'risk': 'If scaler was fit on entire dataset, this is leakage',
                    'recommendation': 'Use Pipeline or fit scaler on training data only'
                })
    
    def _check_imputed_features(self):
        """Check if features appear to have been imputed."""
        # Features with suspiciously few NaN values might be imputed
        for col in self.X.columns:
            missing_pct = self.X[col].isnull().sum() / len(self.X) * 100
            
            # If few missing values remain, might be imputed
            if 0 < missing_pct < 0.5:
                self.issues.append({
                    'type': 'possibly_imputed',
                    'feature': col,
                    'severity': 'LOW',
                    'message': f"Feature has very few missing values ({missing_pct:.2f}%)",
                    'evidence': f"Missing: {missing_pct:.2f}%",
                    'risk': 'If imputer was fit on entire dataset, this is leakage',
                    'recommendation': 'Fit imputation strategy on training data only; use Pipeline'
                })
    
    def _check_encoded_features(self):
        """Check for signs of categorical encoding."""
        numeric_cols = self.X.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            col_data = self.X[col]
            
            # If integers with small unique values, likely encoded categorical
            if col_data.dtype in [np.int32, np.int64]:
                n_unique = col_data.nunique()
                
                # If between 2-50 unique integer values, likely encoding
                if 2 <= n_unique <= 50:
                    unique_vals = sorted(col_data.dropna().unique())
                    
                    # Check if sequential (0, 1, 2, ... or 1, 2, 3, ...)
                    is_sequential = (
                        (unique_vals[0] == 0 and unique_vals[-1] == len(unique_vals) - 1) or
                        (unique_vals[0] == 1 and unique_vals[-1] == len(unique_vals))
                    )
                    
                    if is_sequential:
                        self.issues.append({
                            'type': 'likely_encoded',
                            'feature': col,
                            'severity': 'LOW',
                            'message': f"Feature appears to be label-encoded categorical ({n_unique} categories)",
                            'evidence': f"Unique values: {unique_vals}",
                            'risk': 'If encoder was fit on entire dataset, this is leakage',
                            'recommendation': 'Fit encoder on training data only; use Pipeline or OneHotEncoder'
                        })
    
    def get_report(self) -> Dict:
        """
        Generate report.
        
        Returns:
            Dictionary with findings
        """
        high = sum(1 for i in self.issues if i.get('severity') == 'HIGH')
        medium = sum(1 for i in self.issues if i.get('severity') == 'MEDIUM')
        low = sum(1 for i in self.issues if i.get('severity') == 'LOW')
        
        return {
            'total_issues': len(self.issues),
            'high_severity': high,
            'medium_severity': medium,
            'low_severity': low,
            'issues': self.issues,
            'has_risk': len(self.issues) > 0
        }

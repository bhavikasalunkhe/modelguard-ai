"""
Validation Split Checker

Checks train/test split strategy:
- Was random_split used on time series?
- Is validation strategy appropriate?
- Are stratified splits used for imbalanced data?
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


class SplitChecker:
    """Check train/test split strategy."""
    
    def __init__(self, X: pd.DataFrame, y: pd.Series = None):
        """
        Initialize checker.
        
        Args:
            X: Features DataFrame
            y: Target series
        """
        self.X = X
        self.y = y
        self.issues = []
    
    def detect_temporal_column(self) -> Optional[str]:
        """
        Detect if dataset has temporal information.
        
        Returns:
            Column name if temporal column detected, None otherwise
        """
        for col in self.X.columns:
            col_lower = col.lower()
            
            # Check for date-like column names
            if any(x in col_lower for x in ['date', 'time', 'timestamp', 'period', 'year', 'month', 'day']):
                # Try to parse as datetime
                try:
                    pd.to_datetime(self.X[col])
                    return col
                except:
                    pass
        
        return None
    
    def check_split_strategy(self) -> Dict:
        """
        Check if split strategy is appropriate.
        
        Returns:
            Dictionary with findings
        """
        temporal_col = self.detect_temporal_column()
        
        if temporal_col:
            self.issues.append({
                'type': 'temporal_data_detected',
                'severity': 'MEDIUM',
                'message': f"Dataset contains temporal column '{temporal_col}'",
                'evidence': f"Column detected: {temporal_col}",
                'risk': 'Random train/test split may cause leakage; future data may be in training set',
                'recommendation': f'Use time-based split or StratifiedKFold; set aside last X% as test'
            })
        
        # Check class imbalance
        if self.y is not None:
            if self.y.dtype in ['object', 'category'] or self.y.nunique() < 20:
                value_counts = self.y.value_counts(normalize=True)
                min_pct = value_counts.min() * 100
                
                if min_pct < 20:
                    self.issues.append({
                        'type': 'imbalanced_needs_stratification',
                        'severity': 'MEDIUM',
                        'message': 'Imbalanced target; stratified split recommended',
                        'evidence': f"Minority class: {min_pct:.1f}%",
                        'risk': 'Random split may result in unequal class distribution in train/test',
                        'recommendation': 'Use stratified_split=True or StratifiedKFold'
                    })
        
        return self.get_report()
    
    def check_cross_validation(self) -> Dict:
        """
        Check if cross-validation is used.
        
        Returns:
            Recommendations for cross-validation
        """
        findings = {
            'message': 'No code provided for cross-validation check',
            'recommendation': 'Use cross-validation: cross_val_score or KFold',
            'types': {
                'standard': 'KFold or StratifiedKFold',
                'timeseries': 'TimeSeriesSplit',
                'grouped': 'GroupKFold if data has groups'
            }
        }
        
        return findings
    
    def get_report(self) -> Dict:
        """
        Generate report.
        
        Returns:
            Dictionary with split strategy assessment
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
            'has_issues': len(self.issues) > 0
        }

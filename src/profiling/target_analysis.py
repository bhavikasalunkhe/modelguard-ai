"""
Target Variable Analysis Module

Analyzes the target variable:
- Distribution analysis
- Classification vs Regression detection
- Class balance assessment
- Target statistics
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class TargetAnalysis:
    """Analyze target variable characteristics."""
    
    def __init__(self, target: pd.Series, name: str = "target"):
        """
        Initialize target analysis.
        
        Args:
            target: Target series
            name: Name of target variable
        """
        self.target = target
        self.name = name
    
    def analyze(self) -> Dict:
        """
        Perform complete target analysis.
        
        Returns:
            Dictionary with analysis results
        """
        target_type = self.infer_type()
        
        analysis = {
            'name': self.name,
            'type': target_type,
            'n_samples': len(self.target),
            'n_missing': self.target.isnull().sum(),
            'pct_missing': self.target.isnull().sum() / len(self.target) * 100,
            'n_unique': self.target.nunique(),
            'dtype': str(self.target.dtype)
        }
        
        if target_type == 'classification':
            analysis.update(self._analyze_classification())
        else:
            analysis.update(self._analyze_regression())
        
        return analysis
    
    def infer_type(self) -> str:
        """
        Infer whether target is classification or regression.
        
        Returns:
            'classification' or 'regression'
        """
        # Check if numeric
        if pd.api.types.is_numeric_dtype(self.target):
            n_unique = self.target.nunique()
            n_total = len(self.target)
            
            # If few unique values relative to total, likely classification
            if n_unique <= 20 and n_unique / n_total < 0.1:
                return 'classification'
            else:
                return 'regression'
        else:
            # Non-numeric is always classification
            return 'classification'
    
    def _analyze_classification(self) -> Dict:
        """Analyze classification target."""
        value_counts = self.target.value_counts()
        value_counts_pct = self.target.value_counts(normalize=True) * 100
        
        # Build class distribution
        class_dist = {}
        for idx in value_counts.index:
            class_dist[str(idx)] = {
                'count': int(value_counts[idx]),
                'percentage': float(value_counts_pct[idx])
            }
        
        # Calculate imbalance metrics
        min_class_pct = value_counts_pct.min()
        max_class_pct = value_counts_pct.max()
        imbalance_ratio = max_class_pct / min_class_pct if min_class_pct > 0 else np.inf
        
        return {
            'classes': sorted(list(value_counts.index)),
            'n_classes': len(value_counts),
            'class_distribution': class_dist,
            'min_class_percentage': float(min_class_pct),
            'max_class_percentage': float(max_class_pct),
            'imbalance_ratio': float(imbalance_ratio),
            'is_binary': len(value_counts) == 2,
            'is_multiclass': len(value_counts) > 2,
            'is_balanced': min_class_pct >= 40
        }
    
    def _analyze_regression(self) -> Dict:
        """Analyze regression target."""
        target_clean = self.target.dropna()
        
        return {
            'mean': float(target_clean.mean()),
            'median': float(target_clean.median()),
            'std': float(target_clean.std()),
            'min': float(target_clean.min()),
            'max': float(target_clean.max()),
            'q25': float(target_clean.quantile(0.25)),
            'q75': float(target_clean.quantile(0.75)),
            'skewness': float(target_clean.skew()),
            'kurtosis': float(target_clean.kurtosis()),
            'range': float(target_clean.max() - target_clean.min())
        }

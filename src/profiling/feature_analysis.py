"""
Feature Analysis Module

Analyzes features:
- Feature statistics
- Feature types
- Feature distributions
- Missing value patterns
"""

import pandas as pd
import numpy as np
from typing import Dict, List


class FeatureAnalysis:
    """Analyze feature characteristics."""
    
    def __init__(self, X: pd.DataFrame):
        """
        Initialize feature analysis.
        
        Args:
            X: Features DataFrame
        """
        self.X = X
    
    def analyze(self) -> Dict:
        """
        Perform complete feature analysis.
        
        Returns:
            Dictionary with analysis results
        """
        numeric_cols = self.X.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.X.select_dtypes(include=['object', 'category']).columns.tolist()
        
        analysis = {
            'n_features': len(self.X.columns),
            'n_rows': len(self.X),
            'n_numeric': len(numeric_cols),
            'n_categorical': len(categorical_cols),
            'memory_mb': float(self.X.memory_usage(deep=True).sum() / 1024**2),
            'numeric_features': numeric_cols,
            'categorical_features': categorical_cols,
            'numeric_analysis': self._analyze_numeric(numeric_cols),
            'categorical_analysis': self._analyze_categorical(categorical_cols)
        }
        
        return analysis
    
    def _analyze_numeric(self, numeric_cols: List) -> Dict:
        """Analyze numeric features."""
        if not numeric_cols:
            return {}
        
        numeric_data = self.X[numeric_cols]
        
        stats = {}
        for col in numeric_cols:
            col_data = numeric_data[col]
            
            stats[col] = {
                'dtype': str(col_data.dtype),
                'missing_count': int(col_data.isnull().sum()),
                'missing_pct': float(col_data.isnull().sum() / len(col_data) * 100),
                'mean': float(col_data.mean()) if not col_data.isnull().all() else None,
                'median': float(col_data.median()) if not col_data.isnull().all() else None,
                'std': float(col_data.std()) if not col_data.isnull().all() else None,
                'min': float(col_data.min()) if not col_data.isnull().all() else None,
                'max': float(col_data.max()) if not col_data.isnull().all() else None,
                'q25': float(col_data.quantile(0.25)) if not col_data.isnull().all() else None,
                'q75': float(col_data.quantile(0.75)) if not col_data.isnull().all() else None,
                'skewness': float(col_data.skew()) if not col_data.isnull().all() else None,
                'unique_values': int(col_data.nunique()),
            }
        
        return stats
    
    def _analyze_categorical(self, categorical_cols: List) -> Dict:
        """Analyze categorical features."""
        if not categorical_cols:
            return {}
        
        stats = {}
        for col in categorical_cols:
            col_data = self.X[col]
            value_counts = col_data.value_counts()
            
            stats[col] = {
                'dtype': str(col_data.dtype),
                'missing_count': int(col_data.isnull().sum()),
                'missing_pct': float(col_data.isnull().sum() / len(col_data) * 100),
                'unique_values': int(col_data.nunique()),
                'most_common': str(value_counts.index[0]) if len(value_counts) > 0 else None,
                'most_common_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else None,
                'most_common_pct': float(value_counts.iloc[0] / len(col_data) * 100) if len(value_counts) > 0 else None,
                'top_10_values': dict(value_counts.head(10))
            }
        
        return stats

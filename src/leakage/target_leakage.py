"""
Target Leakage Detector

Detects features that may contain leaked information about target variable:
- High correlations with target
- Suspicious feature names
- Features with information not available at prediction time
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from scipy.stats import spearmanr


class TargetLeakageDetector:
    """Detect potential target leakage in features."""
    
    # Feature names that suggest leakage
    LEAKAGE_KEYWORDS = [
        'target', 'outcome', 'result', 'label',
        'final_score', 'final', 'actual', 'true',
        'prediction', 'pred', 'forecast', 'forecast_result',
        'y_', 'answer', 'ground_truth', 'groundtruth',
        'payment_status', 'churn_date', 'cancellation', 'exit',
        'post_', 'after_', 'during_', 'future_', '_future',
        'event_', 'incident_', 'claim_', 'default_',
        'approved', 'rejected', 'declined', 'accepted',
        'revenue_after', 'sales_final', 'profit_actual'
    ]
    
    def __init__(self, X: pd.DataFrame, y: pd.Series, name: str = "target"):
        """
        Initialize leakage detector.
        
        Args:
            X: Features DataFrame
            y: Target series
            name: Name of target variable
        """
        self.X = X
        self.y = y
        self.name = name
        self.leakage_candidates = []
    
    def detect(self) -> Dict:
        """
        Detect target leakage.
        
        Returns:
            Dictionary with leakage detection results
        """
        self._check_suspicious_names()
        self._check_high_correlations()
        self._check_information_content()
        
        return self.get_report()
    
    def _check_suspicious_names(self):
        """Check for suspicious feature names."""
        for col in self.X.columns:
            col_lower = col.lower()
            
            # Check if name contains leakage keywords
            for keyword in self.LEAKAGE_KEYWORDS:
                if keyword in col_lower:
                    self.leakage_candidates.append({
                        'type': 'suspicious_name',
                        'feature': col,
                        'keyword': keyword,
                        'confidence': 0.7,
                        'message': f"Feature name '{col}' contains keyword '{keyword}'",
                        'recommendation': 'Review feature; it may encode the target or future information'
                    })
                    break
    
    def _check_high_correlations(self):
        """Check for high correlations with target."""
        numeric_cols = self.X.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            # Calculate correlation
            valid_idx = ~(self.X[col].isnull() | self.y.isnull())
            if valid_idx.sum() < 10:
                continue
            
            x_clean = self.X.loc[valid_idx, col]
            y_clean = self.y.loc[valid_idx]
            
            try:
                correlation, p_value = spearmanr(x_clean, y_clean)
                
                # High absolute correlation suggests leakage
                if abs(correlation) > 0.8:
                    confidence = min(0.99, 0.7 + abs(correlation) * 0.2)
                    
                    self.leakage_candidates.append({
                        'type': 'high_correlation',
                        'feature': col,
                        'correlation': float(correlation),
                        'p_value': float(p_value),
                        'confidence': float(confidence),
                        'message': f"Feature has high correlation ({correlation:.3f}) with target",
                        'recommendation': 'Verify this feature is available at prediction time'
                    })
            except:
                pass
    
    def _check_information_content(self):
        """Check if features have optimal information content."""
        for col in self.X.columns:
            # Very high variance might indicate leakage
            if self.X[col].dtype in ['object', 'category']:
                # For categorical, check uniqueness
                n_unique = self.X[col].nunique()
                if n_unique > len(self.X) * 0.5:
                    # Each row almost unique - might be ID or timestamp
                    if any(x in col.lower() for x in ['id', 'code', 'date', 'time', 'timestamp']):
                        self.leakage_candidates.append({
                            'type': 'quasi_identifier',
                            'feature': col,
                            'confidence': 0.5,
                            'message': f"Feature appears to be identifier (high cardinality: {n_unique})",
                            'recommendation': 'Remove identifiers and time-based features'
                        })
    
    def get_report(self) -> Dict:
        """
        Generate leakage detection report.
        
        Returns:
            Dictionary with leakage assessment
        """
        n_candidates = len(self.leakage_candidates)
        
        # Sort by confidence
        sorted_candidates = sorted(
            self.leakage_candidates,
            key=lambda x: x.get('confidence', 0),
            reverse=True
        )
        
        return {
            'total_candidates': n_candidates,
            'high_risk': sum(1 for c in sorted_candidates if c.get('confidence', 0) > 0.8),
            'medium_risk': sum(1 for c in sorted_candidates if 0.5 <= c.get('confidence', 0) <= 0.8),
            'low_risk': sum(1 for c in sorted_candidates if c.get('confidence', 0) < 0.5),
            'candidates': sorted_candidates,
            'has_leakage': n_candidates > 0
        }

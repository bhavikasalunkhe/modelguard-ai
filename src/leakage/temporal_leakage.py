"""
Temporal Leakage Detector

Detects when temporal features contain information from the future.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


class TemporalLeakageDetector:
    """Detect temporal leakage."""
    
    TEMPORAL_KEYWORDS = ['date', 'time', 'timestamp', 'period', 'year', 'month', 'day', 'hour', 'minute']
    
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
        Detect temporal leakage.
        
        Returns:
            Dictionary with detection results
        """
        self._find_temporal_features()
        self._check_temporal_ordering()
        self._check_feature_timing()
        
        return self.get_report()
    
    def _find_temporal_features(self):
        """Identify temporal features."""
        temporal_features = []
        
        for col in self.X.columns:
            col_lower = col.lower()
            
            # Check name
            if any(keyword in col_lower for keyword in self.TEMPORAL_KEYWORDS):
                temporal_features.append(col)
            
            # Try to parse as datetime
            try:
                pd.to_datetime(self.X[col])
                temporal_features.append(col)
            except:
                pass
        
        self.temporal_features = temporal_features
    
    def _check_temporal_ordering(self):
        """Check if temporal features show proper ordering."""
        for col in self.temporal_features:
            try:
                dates = pd.to_datetime(self.X[col])
                
                # Check if sorted (should be if time series)
                if not (dates.diff().dropna() >= pd.Timedelta(0)).all():
                    self.issues.append({
                        'type': 'unsorted_temporal',
                        'feature': col,
                        'severity': 'MEDIUM',
                        'message': 'Temporal feature not in chronological order',
                        'evidence': 'Dates appear out of order',
                        'risk': 'Random train/test split would cause leakage',
                        'recommendation': 'Use time-based train/test split (e.g., train on past, test on future)'
                    })
            except:
                pass
    
    def _check_feature_timing(self):
        """Check if features are available at prediction time."""
        if not self.temporal_features:
            return
        
        for col in self.X.columns:
            col_lower = col.lower()
            
            # Check for features that might be post-event
            if any(x in col_lower for x in ['post_', 'after_', 'subsequent_', 'following_']):
                self.issues.append({
                    'type': 'post_event_feature',
                    'feature': col,
                    'severity': 'HIGH',
                    'message': f"Feature '{col}' may contain post-event information",
                    'evidence': f"Feature name suggests temporal ordering issue",
                    'risk': 'High risk of leakage; information may not be available at prediction time',
                    'recommendation': 'Verify this feature is available before the target occurs'
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
            'temporal_features': self.temporal_features,
            'issues': self.issues,
            'has_temporal_data': len(self.temporal_features) > 0
        }

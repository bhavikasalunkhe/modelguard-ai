"""
Calibration Checker

Checks prediction probability calibration.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional


class CalibrationChecker:
    """Check model probability calibration."""
    
    def __init__(self, y_true: pd.Series, y_pred_proba: pd.Series):
        """
        Initialize checker.
        
        Args:
            y_true: True labels
            y_pred_proba: Predicted probabilities
        """
        self.y_true = y_true
        self.y_pred_proba = y_pred_proba
    
    def check_calibration(self) -> Dict:
        """
        Check if probabilities are well-calibrated.
        
        Returns:
            Dictionary with calibration analysis
        """
        # Group probabilities into bins
        bins = np.linspace(0, 1, 11)  # 0-10%, 10-20%, ..., 90-100%
        bin_centers = (bins[:-1] + bins[1:]) / 2
        
        calibration_data = []
        
        for i in range(len(bins) - 1):
            mask = (self.y_pred_proba >= bins[i]) & (self.y_pred_proba < bins[i+1])
            
            if mask.sum() > 0:
                avg_pred = self.y_pred_proba[mask].mean()
                avg_true = self.y_true[mask].mean()
                
                calibration_data.append({
                    'bin': f"{bins[i]:.0%}-{bins[i+1]:.0%}",
                    'avg_pred_prob': float(avg_pred),
                    'avg_true_freq': float(avg_true),
                    'count': int(mask.sum())
                })
        
        # Calculate expected calibration error (ECE)
        ece = self._calculate_ece()
        
        return {
            'calibration_data': calibration_data,
            'expected_calibration_error': ece,
            'interpretation': self._interpret_calibration(ece),
            'is_well_calibrated': ece < 0.1
        }
    
    def _calculate_ece(self) -> float:
        """Calculate Expected Calibration Error."""
        try:
            bins = np.linspace(0, 1, 11)
            ece = 0
            total_samples = 0
            
            for i in range(len(bins) - 1):
                mask = (self.y_pred_proba >= bins[i]) & (self.y_pred_proba < bins[i+1])
                
                if mask.sum() > 0:
                    avg_pred = self.y_pred_proba[mask].mean()
                    avg_true = self.y_true[mask].mean()
                    
                    ece += abs(avg_pred - avg_true) * mask.sum()
                    total_samples += mask.sum()
            
            return ece / total_samples if total_samples > 0 else 0
        except:
            return None
    
    def _interpret_calibration(self, ece: float) -> str:
        """Interpret calibration quality."""
        if ece is None:
            return "Unable to calculate ECE"
        
        if ece < 0.05:
            return "Excellent calibration"
        elif ece < 0.1:
            return "Good calibration"
        elif ece < 0.2:
            return "Acceptable calibration"
        else:
            return "Poor calibration - consider recalibration"

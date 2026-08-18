"""
Regression Metrics Evaluator

Calculates regression metrics:
- MAE, RMSE, R²
- MAPE
- Residual analysis
"""

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from typing import Dict, Optional


class RegressionEvaluator:
    """Evaluate regression model performance."""
    
    def __init__(self, y_true: pd.Series, y_pred: pd.Series):
        """
        Initialize evaluator.
        
        Args:
            y_true: True values
            y_pred: Predicted values
        """
        self.y_true = y_true
        self.y_pred = y_pred
        self.metrics = {}
    
    def evaluate(self) -> Dict:
        """
        Calculate all regression metrics.
        
        Returns:
            Dictionary with all metrics
        """
        self._calculate_error_metrics()
        self._calculate_percentage_metrics()
        self._calculate_residual_metrics()
        
        return self.get_report()
    
    def _calculate_error_metrics(self):
        """Calculate error metrics."""
        try:
            self.metrics['mae'] = float(mean_absolute_error(self.y_true, self.y_pred))
        except:
            self.metrics['mae'] = None
        
        try:
            self.metrics['rmse'] = float(np.sqrt(mean_squared_error(self.y_true, self.y_pred)))
        except:
            self.metrics['rmse'] = None
        
        try:
            self.metrics['mse'] = float(mean_squared_error(self.y_true, self.y_pred))
        except:
            self.metrics['mse'] = None
        
        try:
            self.metrics['r2'] = float(r2_score(self.y_true, self.y_pred))
        except:
            self.metrics['r2'] = None
    
    def _calculate_percentage_metrics(self):
        """Calculate percentage-based metrics."""
        try:
            # Only calculate MAPE if all values are non-zero
            if (self.y_true == 0).any():
                self.metrics['mape'] = None
            else:
                self.metrics['mape'] = float(mean_absolute_percentage_error(self.y_true, self.y_pred))
        except:
            self.metrics['mape'] = None
    
    def _calculate_residual_metrics(self):
        """Calculate residual statistics."""
        try:
            residuals = self.y_true - self.y_pred
            
            self.metrics['residual_mean'] = float(residuals.mean())
            self.metrics['residual_std'] = float(residuals.std())
            self.metrics['residual_min'] = float(residuals.min())
            self.metrics['residual_max'] = float(residuals.max())
        except:
            pass
    
    def get_report(self) -> Dict:
        """
        Generate evaluation report.
        
        Returns:
            Dictionary with all metrics and interpretation
        """
        warnings = []
        
        # Check for issues
        if self.metrics.get('r2') is not None:
            if self.metrics['r2'] < 0.5:
                warnings.append(f"⚠️  Low R² ({self.metrics['r2']:.3f}): Model explains less than 50% of variance")
            
            if self.metrics['r2'] < 0:
                warnings.append("⚠️  Negative R²: Model performs worse than predicting mean")
        
        if self.metrics.get('mae') is not None and self.metrics.get('rmse') is not None:
            if self.metrics['rmse'] > self.metrics['mae'] * 2:
                warnings.append("⚠️  High outliers: RMSE much larger than MAE")
        
        return {
            'metrics': {k: v for k, v in self.metrics.items() if v is not None},
            'warnings': warnings,
            'interpretation': self._interpret_metrics()
        }
    
    def _interpret_metrics(self) -> str:
        """Interpret metrics."""
        r2 = self.metrics.get('r2')
        
        if r2 is None:
            return "Unable to calculate metrics"
        
        if r2 > 0.8:
            return "Excellent fit"
        elif r2 > 0.6:
            return "Good fit"
        elif r2 > 0.4:
            return "Acceptable fit"
        elif r2 > 0.2:
            return "Fair fit"
        else:
            return "Poor fit"

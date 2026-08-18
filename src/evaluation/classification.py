"""
Classification Metrics Evaluator

Calculates comprehensive classification metrics:
- Accuracy, Precision, Recall, F1
- ROC-AUC, PR-AUC
- Log Loss, Brier Score
- Confusion Matrix
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, log_loss, brier_score_loss,
    confusion_matrix, precision_recall_curve, roc_curve
)
from typing import Dict, Tuple, Optional


class ClassificationEvaluator:
    """Evaluate classification model performance."""
    
    def __init__(self, y_true: pd.Series, y_pred: pd.Series, 
                 y_pred_proba: Optional[pd.DataFrame] = None):
        """
        Initialize evaluator.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_pred_proba: Predicted probabilities (for AUC calculation)
        """
        self.y_true = y_true
        self.y_pred = y_pred
        self.y_pred_proba = y_pred_proba
        self.metrics = {}
    
    def evaluate(self) -> Dict:
        """
        Calculate all classification metrics.
        
        Returns:
            Dictionary with all metrics
        """
        self._calculate_basic_metrics()
        self._calculate_advanced_metrics()
        self._calculate_confusion_matrix()
        
        return self.get_report()
    
    def _calculate_basic_metrics(self):
        """Calculate basic metrics."""
        try:
            self.metrics['accuracy'] = float(accuracy_score(self.y_true, self.y_pred))
        except:
            self.metrics['accuracy'] = None
        
        # Determine if binary or multiclass
        is_binary = len(np.unique(self.y_true)) == 2
        average_type = 'binary' if is_binary else 'weighted'
        
        try:
            self.metrics['precision'] = float(precision_score(
                self.y_true, self.y_pred, average=average_type, zero_division=0
            ))
        except:
            self.metrics['precision'] = None
        
        try:
            self.metrics['recall'] = float(recall_score(
                self.y_true, self.y_pred, average=average_type, zero_division=0
            ))
        except:
            self.metrics['recall'] = None
        
        try:
            self.metrics['f1'] = float(f1_score(
                self.y_true, self.y_pred, average=average_type, zero_division=0
            ))
        except:
            self.metrics['f1'] = None
    
    def _calculate_advanced_metrics(self):
        """Calculate advanced metrics (AUC, log loss)."""
        is_binary = len(np.unique(self.y_true)) == 2
        
        # ROC-AUC
        try:
            if self.y_pred_proba is not None:
                if is_binary:
                    # Use probability of positive class
                    y_proba = self.y_pred_proba.iloc[:, 1] if self.y_pred_proba.shape[1] > 1 else self.y_pred_proba.iloc[:, 0]
                    self.metrics['roc_auc'] = float(roc_auc_score(self.y_true, y_proba))
                else:
                    # Multiclass
                    self.metrics['roc_auc'] = float(roc_auc_score(
                        self.y_true, self.y_pred_proba, multi_class='ovr', labels=np.unique(self.y_true)
                    ))
            else:
                self.metrics['roc_auc'] = None
        except:
            self.metrics['roc_auc'] = None
        
        # PR-AUC (Average Precision)
        try:
            if self.y_pred_proba is not None and is_binary:
                y_proba = self.y_pred_proba.iloc[:, 1] if self.y_pred_proba.shape[1] > 1 else self.y_pred_proba.iloc[:, 0]
                self.metrics['pr_auc'] = float(average_precision_score(self.y_true, y_proba))
            else:
                self.metrics['pr_auc'] = None
        except:
            self.metrics['pr_auc'] = None
        
        # Log Loss
        try:
            if self.y_pred_proba is not None:
                self.metrics['log_loss'] = float(log_loss(self.y_true, self.y_pred_proba))
            else:
                self.metrics['log_loss'] = None
        except:
            self.metrics['log_loss'] = None
        
        # Brier Score
        try:
            if self.y_pred_proba is not None and is_binary:
                y_proba = self.y_pred_proba.iloc[:, 1] if self.y_pred_proba.shape[1] > 1 else self.y_pred_proba.iloc[:, 0]
                self.metrics['brier_score'] = float(brier_score_loss(self.y_true, y_proba))
            else:
                self.metrics['brier_score'] = None
        except:
            self.metrics['brier_score'] = None
    
    def _calculate_confusion_matrix(self):
        """Calculate confusion matrix."""
        try:
            cm = confusion_matrix(self.y_true, self.y_pred)
            self.metrics['confusion_matrix'] = cm.tolist()
            
            # For binary classification, calculate specific metrics
            if len(cm) == 2:
                tn, fp, fn, tp = cm.ravel()
                self.metrics['true_positives'] = int(tp)
                self.metrics['true_negatives'] = int(tn)
                self.metrics['false_positives'] = int(fp)
                self.metrics['false_negatives'] = int(fn)
                self.metrics['specificity'] = float(tn / (tn + fp)) if (tn + fp) > 0 else None
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
        if self.metrics.get('accuracy') is not None:
            if self.metrics['recall'] is not None and self.metrics['recall'] < 0.5:
                warnings.append(
                    f"⚠️  Low Recall ({self.metrics['recall']:.1%}): "
                    f"Model misses {(1-self.metrics['recall'])*100:.0f}% of positive cases"
                )
            
            if self.metrics['precision'] is not None and self.metrics['precision'] < 0.5:
                warnings.append(
                    f"⚠️  Low Precision ({self.metrics['precision']:.1%}): "
                    f"Model produces many false positives"
                )
        
        return {
            'metrics': {k: v for k, v in self.metrics.items() if v is not None},
            'warnings': warnings,
            'interpretation': self._interpret_metrics()
        }
    
    def _interpret_metrics(self) -> str:
        """Interpret metrics."""
        if self.metrics['f1'] is None:
            return "Unable to calculate metrics"
        
        f1 = self.metrics['f1']
        accuracy = self.metrics.get('accuracy', 0)
        
        if f1 > 0.8:
            return "Excellent performance"
        elif f1 > 0.7:
            return "Good performance"
        elif f1 > 0.6:
            return "Acceptable performance"
        elif f1 > 0.5:
            return "Fair performance"
        else:
            return "Poor performance"

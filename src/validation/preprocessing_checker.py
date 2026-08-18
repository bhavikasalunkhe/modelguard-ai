"""
Preprocessing Checker

Validates preprocessing practices.
"""

from typing import Dict, List


class PreprocessingChecker:
    """Check preprocessing implementation."""
    
    def __init__(self):
        """Initialize checker."""
        self.issues = []
    
    def check(self) -> Dict:
        """
        Provide preprocessing recommendations.
        
        Returns:
            Dictionary with recommendations
        """
        return {
            'best_practices': self._get_best_practices(),
            'common_mistakes': self._get_common_mistakes()
        }
    
    def _get_best_practices(self) -> List[str]:
        """Get preprocessing best practices."""
        return [
            'Use sklearn Pipeline to prevent data leakage',
            'Fit all transformers on training data only',
            'Apply fitted transformers to test data',
            'Use cross-validation to validate entire pipeline',
            'Handle missing values consistently across train/test',
            'Apply feature scaling after train/test split',
            'One-hot encode categorical variables safely',
            'Document all preprocessing steps'
        ]
    
    def _get_common_mistakes(self) -> List[Dict]:
        """Get common preprocessing mistakes."""
        return [
            {
                'mistake': 'Fit scaler on entire dataset',
                'impact': 'Data leakage - test data affects scaling',
                'solution': 'Fit scaler only on training data'
            },
            {
                'mistake': 'Impute missing values before split',
                'impact': 'Leakage - test data affects imputation',
                'solution': 'Impute training data, use those parameters for test'
            },
            {
                'mistake': 'Remove outliers before split',
                'impact': 'Information leakage',
                'solution': 'Define outliers using training data only'
            },
            {
                'mistake': 'Perform feature selection on full data',
                'impact': 'Selection bias - test features chosen on test data',
                'solution': 'Feature selection inside cross-validation'
            },
            {
                'mistake': 'One-hot encode before split',
                'impact': 'Categories in test might differ from train',
                'solution': 'Use ColumnTransformer in Pipeline'
            }
        ]

"""
ModelGuard Reliability Score

Custom scoring framework:
- Data Quality: 20 points
- Validation: 20 points
- Leakage Risk: 20 points
- Model Performance: 20 points
- Explainability: 10 points
- Reproducibility: 10 points

Total: 100 points
"""

from typing import Dict
import math


class ReliabilityScorer:
    """Calculate ModelGuard Reliability Score."""
    
    # Maximum points per category
    WEIGHTS = {
        'data_quality': 20,
        'validation': 20,
        'leakage': 20,
        'performance': 20,
        'explainability': 10,
        'reproducibility': 10
    }
    
    # Risk thresholds
    RISK_THRESHOLDS = {
        'low_risk': (80, 100),      # 80-100: Low risk
        'review_required': (60, 79), # 60-79: Review required
        'high_risk': (0, 59)         # 0-59: High risk
    }
    
    def __init__(self):
        """Initialize scorer."""
        self.scores = {}
    
    def calculate(self, audit_results: Dict) -> Dict:
        """
        Calculate overall reliability score.
        
        Args:
            audit_results: Dictionary containing all audit results
            
        Returns:
            Dictionary with score breakdown and status
        """
        # Extract scores from audit results
        data_quality_score = self._score_data_quality(
            audit_results.get('data_quality', {})
        )
        validation_score = self._score_validation(
            audit_results.get('validation', {})
        )
        leakage_score = self._score_leakage(
            audit_results.get('leakage', {})
        )
        performance_score = self._score_performance(
            audit_results.get('performance', {})
        )
        explainability_score = self._score_explainability(
            audit_results.get('explainability', {})
        )
        reproducibility_score = self._score_reproducibility(
            audit_results.get('reproducibility', {})
        )
        
        # Store component scores
        self.scores = {
            'data_quality': data_quality_score,
            'validation': validation_score,
            'leakage': leakage_score,
            'performance': performance_score,
            'explainability': explainability_score,
            'reproducibility': reproducibility_score
        }
        
        # Calculate total
        total_score = sum(self.scores.values())
        
        # Determine risk status
        status, icon = self._get_status(total_score)
        
        return {
            'total_score': round(total_score, 1),
            'max_score': 100,
            'scores': {
                'data_quality': {
                    'score': round(data_quality_score, 1),
                    'max': self.WEIGHTS['data_quality']
                },
                'validation': {
                    'score': round(validation_score, 1),
                    'max': self.WEIGHTS['validation']
                },
                'leakage': {
                    'score': round(leakage_score, 1),
                    'max': self.WEIGHTS['leakage']
                },
                'performance': {
                    'score': round(performance_score, 1),
                    'max': self.WEIGHTS['performance']
                },
                'explainability': {
                    'score': round(explainability_score, 1),
                    'max': self.WEIGHTS['explainability']
                },
                'reproducibility': {
                    'score': round(reproducibility_score, 1),
                    'max': self.WEIGHTS['reproducibility']
                }
            },
            'status': status,
            'status_icon': icon,
            'interpretation': self._interpret_score(total_score)
        }
    
    def _score_data_quality(self, results: Dict) -> float:
        """Score data quality (0-20)."""
        if not results:
            return 0
        
        quality_score = results.get('quality_score', 0)
        # Convert 0-100 scale to 0-20
        return (quality_score / 100) * self.WEIGHTS['data_quality']
    
    def _score_validation(self, results: Dict) -> float:
        """Score validation strategy (0-20)."""
        if not results:
            return 10  # Neutral if no info
        
        score = self.WEIGHTS['validation']
        
        # Penalize for issues
        issues = results.get('issues', [])
        for issue in issues:
            severity = issue.get('severity', 'LOW')
            if severity == 'HIGH':
                score -= 8
            elif severity == 'MEDIUM':
                score -= 4
            elif severity == 'LOW':
                score -= 2
        
        return max(0, score)
    
    def _score_leakage(self, results: Dict) -> float:
        """Score leakage detection (0-20)."""
        if not results:
            return 20  # Full points if no leakage
        
        candidates = results.get('candidates', [])
        score = self.WEIGHTS['leakage']
        
        for candidate in candidates:
            confidence = candidate.get('confidence', 0.5)
            # Higher confidence = more penalty
            penalty = confidence * 8
            score -= penalty
        
        return max(0, score)
    
    def _score_performance(self, results: Dict) -> float:
        """Score model performance (0-20)."""
        if not results or not results.get('metrics'):
            return 0
        
        metrics = results['metrics']
        
        # Base score on F1 or accuracy
        f1 = metrics.get('f1', 0)
        accuracy = metrics.get('accuracy', 0)
        
        # Use F1 if available, otherwise accuracy
        perf_metric = f1 if f1 is not None else accuracy
        
        # Convert 0-1 scale to 0-20
        score = perf_metric * self.WEIGHTS['performance']
        
        return max(0, score)
    
    def _score_explainability(self, results: Dict) -> float:
        """Score explainability (0-10)."""
        # If SHAP available, give points
        if results and results.get('has_explanations'):
            return self.WEIGHTS['explainability']
        
        # Partial credit for having predictions
        if results and results.get('has_predictions'):
            return self.WEIGHTS['explainability'] * 0.5
        
        return 0
    
    def _score_reproducibility(self, results: Dict) -> float:
        """Score reproducibility (0-10)."""
        if not results:
            return 0
        
        score = 0
        
        # Points for each reproducibility factor
        if results.get('has_code'):
            score += 3
        if results.get('has_documentation'):
            score += 3
        if results.get('has_version_info'):
            score += 2
        if results.get('has_seeds'):
            score += 2
        
        return min(score, self.WEIGHTS['reproducibility'])
    
    def _get_status(self, score: float) -> tuple:
        """
        Determine status from score.
        
        Returns:
            Tuple of (status_text, icon)
        """
        if 80 <= score <= 100:
            return "🟢 LOW RISK", "🟢"
        elif 60 <= score < 80:
            return "🟠 REVIEW REQUIRED", "🟠"
        else:
            return "🔴 HIGH RISK", "🔴"
    
    def _interpret_score(self, score: float) -> str:
        """Interpret score."""
        if score >= 90:
            return "Excellent: Model appears reliable and well-validated"
        elif score >= 80:
            return "Good: Model has acceptable quality with minor issues"
        elif score >= 70:
            return "Fair: Model needs review; some issues detected"
        elif score >= 60:
            return "Poor: Model has significant issues requiring attention"
        else:
            return "Unacceptable: Major problems; do not deploy"

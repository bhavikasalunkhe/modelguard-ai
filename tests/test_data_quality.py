"""
Unit tests for Data Quality Auditor
"""

import pytest
import pandas as pd
import numpy as np
from src.profiling.data_quality import DataQualityAuditor


class TestDataQualityAuditor:
    """Test cases for DataQualityAuditor."""
    
    @pytest.fixture
    def clean_data(self):
        """Create clean test data."""
        return pd.DataFrame({
            'age': [25, 30, 35, 40],
            'income': [35000, 45000, 55000, 65000],
            'target': [0, 1, 0, 1]
        })
    
    @pytest.fixture
    def data_with_missing(self):
        """Create data with missing values."""
        return pd.DataFrame({
            'age': [25, 30, np.nan, 40],
            'income': [35000, np.nan, 55000, 65000],
            'target': [0, 1, 0, 1]
        })
    
    @pytest.fixture
    def data_with_duplicates(self):
        """Create data with duplicates."""
        return pd.DataFrame({
            'age': [25, 25, 30, 40],
            'income': [35000, 35000, 45000, 65000],
            'target': [0, 0, 1, 1]
        })
    
    @pytest.fixture
    def imbalanced_data(self):
        """Create imbalanced data."""
        data = pd.DataFrame({
            'feature': range(100),
            'target': [1] * 95 + [0] * 5
        })
        return data
    
    def test_clean_data_passes(self, clean_data):
        """Test that clean data gets high score."""
        auditor = DataQualityAuditor(clean_data, target_column='target')
        report = auditor.audit()
        
        assert report['quality_score'] >= 80
        assert report['total_issues'] <= 2
    
    def test_missing_values_detection(self, data_with_missing):
        """Test detection of missing values."""
        auditor = DataQualityAuditor(data_with_missing, target_column='target')
        report = auditor.audit()
        
        # Should detect missing values
        missing_issues = [i for i in report['issues'] if i['check_name'] == 'Missing Values']
        assert len(missing_issues) > 0
    
    def test_duplicate_detection(self, data_with_duplicates):
        """Test detection of duplicates."""
        auditor = DataQualityAuditor(data_with_duplicates, target_column='target')
        report = auditor.audit()
        
        # Should detect duplicates
        dup_issues = [i for i in report['issues'] if i['check_name'] == 'Duplicate Records']
        assert len(dup_issues) > 0
    
    def test_imbalance_detection(self, imbalanced_data):
        """Test detection of class imbalance."""
        auditor = DataQualityAuditor(imbalanced_data, target_column='target')
        report = auditor.audit()
        
        # Should detect imbalance
        imb_issues = [i for i in report['issues'] if i['check_name'] == 'Class Imbalance']
        assert len(imb_issues) > 0
        assert imb_issues[0]['severity'] == 'HIGH'
    
    def test_constant_column_detection(self):
        """Test detection of constant columns."""
        data = pd.DataFrame({
            'constant': [1, 1, 1, 1],
            'variable': [1, 2, 3, 4],
            'target': [0, 1, 0, 1]
        })
        
        auditor = DataQualityAuditor(data, target_column='target')
        report = auditor.audit()
        
        # Should detect constant column
        const_issues = [i for i in report['issues'] if i['check_name'] == 'Constant Column']
        assert len(const_issues) > 0
    
    def test_quality_score_calculation(self, clean_data):
        """Test quality score calculation."""
        auditor = DataQualityAuditor(clean_data, target_column='target')
        report = auditor.audit()
        
        # Score should be between 0-100
        assert 0 <= report['quality_score'] <= 100
    
    def test_report_structure(self, clean_data):
        """Test report has correct structure."""
        auditor = DataQualityAuditor(clean_data, target_column='target')
        report = auditor.audit()
        
        assert 'quality_score' in report
        assert 'total_issues' in report
        assert 'high_severity' in report
        assert 'medium_severity' in report
        assert 'low_severity' in report
        assert 'issues' in report


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

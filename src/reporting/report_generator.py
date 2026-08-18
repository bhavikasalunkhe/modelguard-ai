"""
Report Generator Module

Generate comprehensive ModelGuard AI reports in multiple formats.
"""

import json
from typing import Dict, Any
from datetime import datetime


class ReportGenerator:
    """Generate audit reports."""
    
    def __init__(self):
        """Initialize report generator."""
        self.timestamp = datetime.now().isoformat()
    
    def generate(self, audit_results: Dict) -> Dict:
        """
        Generate complete report.
        
        Args:
            audit_results: Complete audit results dictionary
            
        Returns:
            Formatted report dictionary
        """
        report = {
            'metadata': {
                'timestamp': self.timestamp,
                'tool': 'ModelGuard AI',
                'version': '1.0.0'
            },
            'summary': self._generate_summary(audit_results),
            'details': audit_results,
            'recommendations': self._generate_recommendations(audit_results)
        }
        
        return report
    
    def _generate_summary(self, audit_results: Dict) -> Dict:
        """Generate executive summary."""
        reliability_score = audit_results.get('reliability_score', {})
        
        summary = {
            'overall_score': reliability_score.get('total_score', 0),
            'status': reliability_score.get('status', 'Unknown'),
            'interpretation': reliability_score.get('interpretation', ''),
            'high_risk_count': 0,
            'medium_risk_count': 0,
            'low_risk_count': 0
        }
        
        # Count issues across all categories
        for category in ['data_quality', 'validation', 'leakage']:
            results = audit_results.get(category, {})
            issues = results.get('issues', [])
            
            for issue in issues:
                severity = issue.get('severity', 'LOW')
                if severity == 'HIGH':
                    summary['high_risk_count'] += 1
                elif severity == 'MEDIUM':
                    summary['medium_risk_count'] += 1
                elif severity == 'LOW':
                    summary['low_risk_count'] += 1
        
        return summary
    
    def _generate_recommendations(self, audit_results: Dict) -> list:
        """Generate prioritized recommendations."""
        recommendations = []
        
        # Collect all recommendations
        for category in ['data_quality', 'validation', 'leakage']:
            results = audit_results.get(category, {})
            issues = results.get('issues', [])
            
            for issue in issues:
                if 'recommendation' in issue:
                    recommendations.append({
                        'category': category,
                        'severity': issue.get('severity', 'LOW'),
                        'issue': issue.get('message', ''),
                        'action': issue['recommendation']
                    })
        
        # Sort by severity
        severity_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        recommendations.sort(
            key=lambda x: severity_order.get(x['severity'], 3)
        )
        
        return recommendations
    
    def export_json(self, report: Dict, filepath: str):
        """
        Export report to JSON.
        
        Args:
            report: Report dictionary
            filepath: Output file path
        """
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
    
    def export_text(self, report: Dict, filepath: str):
        """
        Export report to text.
        
        Args:
            report: Report dictionary
            filepath: Output file path
        """
        lines = []
        
        # Header
        lines.append("=" * 80)
        lines.append("ModelGuard AI - ML Reliability Assessment Report")
        lines.append("=" * 80)
        lines.append("")
        
        # Summary
        summary = report.get('summary', {})
        lines.append("EXECUTIVE SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Overall Score: {summary.get('overall_score', 0):.1f}/100")
        lines.append(f"Status: {summary.get('status', 'Unknown')}")
        lines.append(f"Interpretation: {summary.get('interpretation', '')}")
        lines.append("")
        lines.append(f"Issues Detected:")
        lines.append(f"  HIGH Risk:   {summary.get('high_risk_count', 0)}")
        lines.append(f"  MEDIUM Risk: {summary.get('medium_risk_count', 0)}")
        lines.append(f"  LOW Risk:    {summary.get('low_risk_count', 0)}")
        lines.append("")
        
        # Recommendations
        recommendations = report.get('recommendations', [])
        if recommendations:
            lines.append("RECOMMENDED ACTIONS")
            lines.append("-" * 80)
            for i, rec in enumerate(recommendations[:10], 1):  # Top 10
                lines.append(f"{i}. [{rec.get('severity', 'N/A')}] {rec.get('action', '')}")
            lines.append("")
        
        # Write to file
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
    
    def format_for_display(self, report: Dict) -> str:
        """
        Format report for terminal display.
        
        Args:
            report: Report dictionary
            
        Returns:
            Formatted string
        """
        summary = report.get('summary', {})
        score = summary.get('overall_score', 0)
        status = summary.get('status', 'Unknown')
        
        output = f"""
╔════════════════════════════════════════════════════════════════════╗
║             ModelGuard AI - ML Assessment Report                   ║
╚════════════════════════════════════════════════════════════════════╝

Overall Score: {score:.1f}/100
Status:        {status}

Issues:
  ❌ HIGH:   {summary.get('high_risk_count', 0)}
  ⚠️  MEDIUM:  {summary.get('medium_risk_count', 0)}
  ℹ️  LOW:    {summary.get('low_risk_count', 0)}

{summary.get('interpretation', '')}

Use generate_report() for full details.
        """
        
        return output

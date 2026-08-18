"""
ModelGuard AI - Streamlit Web Application

Main interface for ML model auditing and assessment.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ingestion.dataset_loader import DatasetLoader
from src.profiling.data_quality import DataQualityAuditor
from src.profiling.target_analysis import TargetAnalysis
from src.profiling.feature_analysis import FeatureAnalysis
from src.leakage.target_leakage import TargetLeakageDetector
from src.leakage.preprocessing_leakage import PreprocessingLeakageDetector
from src.validation.split_checker import SplitChecker
from src.evaluation.classification import ClassificationEvaluator
from src.scoring.reliability_score import ReliabilityScorer
from src.reporting.report_generator import ReportGenerator


# Page config
st.set_page_config(
    page_title="ModelGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .high-risk {
        color: #d32f2f;
        font-weight: bold;
    }
    .medium-risk {
        color: #f57c00;
        font-weight: bold;
    }
    .low-risk {
        color: #388e3c;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'target_col' not in st.session_state:
    st.session_state.target_col = None
if 'audit_results' not in st.session_state:
    st.session_state.audit_results = None


def create_sidebar():
    """Create sidebar navigation."""
    st.sidebar.markdown("# 🛡️ ModelGuard AI")
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("""
    **ML Model Auditing Platform**
    
    Detect data leakage, validation errors, and methodology issues.
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Features")
    st.sidebar.markdown("""
    ✅ Data Quality Audit  
    ✅ Leakage Detection  
    ✅ Validation Checks  
    ✅ Performance Analysis  
    ✅ Reliability Score  
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Version")
    st.sidebar.markdown("ModelGuard AI v1.0.0")


def upload_data_section():
    """Data upload section."""
    st.markdown("## 📁 Upload Dataset")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        
        if uploaded_file:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.success(f"✓ File loaded: {uploaded_file.name}")
            st.markdown(f"**Shape:** {st.session_state.df.shape[0]} rows × {st.session_state.df.shape[1]} columns")
    
    with col2:
        if st.session_state.df is not None:
            st.session_state.target_col = st.selectbox(
                "Select target column",
                st.session_state.df.columns,
                key='target_select'
            )
    
    return st.session_state.df is not None and st.session_state.target_col is not None


def data_preview_section():
    """Show data preview."""
    if st.session_state.df is None:
        return
    
    st.markdown("### Data Preview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(st.session_state.df.head(10), use_container_width=True)
    
    with col2:
        info_text = f"""
        **Dataset Info**
        
        Rows: {len(st.session_state.df)}  
        Columns: {len(st.session_state.df.columns)}  
        Memory: {st.session_state.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
        
        **Data Types**
        
        Numeric: {len(st.session_state.df.select_dtypes(include=[np.number]).columns)}  
        Categorical: {len(st.session_state.df.select_dtypes(include=['object']).columns)}
        """
        st.markdown(info_text)


def run_audit():
    """Run complete audit."""
    if st.session_state.df is None or st.session_state.target_col is None:
        st.warning("Please upload data and select target column first")
        return False
    
    st.markdown("## 🔍 Running Audit...")
    
    # Prepare data
    X = st.session_state.df.drop(columns=[st.session_state.target_col])
    y = st.session_state.df[st.session_state.target_col]
    
    # Data Quality Audit
    with st.spinner("Analyzing data quality..."):
        quality_auditor = DataQualityAuditor(st.session_state.df, target_column=st.session_state.target_col)
        quality_results = quality_auditor.audit()
    
    # Target Analysis
    with st.spinner("Analyzing target..."):
        target_analyzer = TargetAnalysis(y, name=st.session_state.target_col)
        target_results = target_analyzer.analyze()
    
    # Feature Analysis
    with st.spinner("Analyzing features..."):
        feature_analyzer = FeatureAnalysis(X)
        feature_results = feature_analyzer.analyze()
    
    # Leakage Detection
    with st.spinner("Detecting leakage..."):
        leakage_detector = TargetLeakageDetector(X, y, name=st.session_state.target_col)
        leakage_results = leakage_detector.detect()
    
    # Preprocessing Leakage
    with st.spinner("Checking preprocessing..."):
        prep_detector = PreprocessingLeakageDetector(X, y)
        prep_results = prep_detector.detect()
    
    # Validation Checks
    with st.spinner("Checking validation strategy..."):
        split_checker = SplitChecker(X, y)
        validation_results = split_checker.check_split_strategy()
    
    # Prepare complete results
    audit_results = {
        'data_quality': quality_results,
        'target': target_results,
        'features': feature_results,
        'leakage': leakage_results,
        'preprocessing': prep_results,
        'validation': validation_results,
        'reliability_score': {}
    }
    
    # Calculate Reliability Score
    with st.spinner("Calculating reliability score..."):
        scorer = ReliabilityScorer()
        score_results = scorer.calculate(audit_results)
        audit_results['reliability_score'] = score_results
    
    st.session_state.audit_results = audit_results
    st.success("✓ Audit complete!")
    
    return True


def display_results():
    """Display audit results."""
    if st.session_state.audit_results is None:
        return
    
    results = st.session_state.audit_results
    
    # SECTION 1: RELIABILITY SCORE
    st.markdown("## 🎯 ModelGuard Reliability Score")
    
    score_data = results['reliability_score']
    total_score = score_data['total_score']
    status = score_data['status']
    icon = score_data['status_icon']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Reliability Score", f"{total_score:.0f}/100", status)
    
    with col2:
        st.metric("Status", icon)
    
    with col3:
        high_issues = sum(1 for cat in ['data_quality', 'leakage', 'validation']
                         for issue in results.get(cat, {}).get('issues', [])
                         if issue.get('severity') == 'HIGH')
        st.metric("HIGH Risk Issues", high_issues)
    
    with col4:
        medium_issues = sum(1 for cat in ['data_quality', 'leakage', 'validation']
                           for issue in results.get(cat, {}).get('issues', [])
                           if issue.get('severity') == 'MEDIUM')
        st.metric("MEDIUM Risk Issues", medium_issues)
    
    # Score breakdown
    st.markdown("### Score Breakdown")
    
    scores = score_data['scores']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        **Data Quality**  
        {scores['data_quality']['score']:.1f}/{scores['data_quality']['max']}
        
        **Validation**  
        {scores['validation']['score']:.1f}/{scores['validation']['max']}
        """)
    
    with col2:
        st.markdown(f"""
        **Leakage Risk**  
        {scores['leakage']['score']:.1f}/{scores['leakage']['max']}
        
        **Performance**  
        {scores['performance']['score']:.1f}/{scores['performance']['max']}
        """)
    
    with col3:
        st.markdown(f"""
        **Explainability**  
        {scores['explainability']['score']:.1f}/{scores['explainability']['max']}
        
        **Reproducibility**  
        {scores['reproducibility']['score']:.1f}/{scores['reproducibility']['max']}
        """)
    
    # SECTION 2: DATA QUALITY
    st.markdown("## 📊 Data Quality Analysis")
    
    quality = results['data_quality']
    quality_score = quality['quality_score']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Data Quality Score", f"{quality_score:.0f}/100", quality['status'])
    
    with col2:
        st.metric("Total Issues", quality['total_issues'])
    
    with col3:
        st.metric("Critical Issues", quality['high_severity'])
    
    # Display issues
    if quality['issues']:
        st.markdown("### Issues Detected")
        
        for issue in quality['issues']:
            severity = issue['severity']
            icon = "🔴" if severity == "HIGH" else "🟠" if severity == "MEDIUM" else "🟡"
            
            with st.expander(f"{icon} {issue['check_name']} - {issue['column']}", expanded=(severity == "HIGH")):
                st.markdown(f"**Message:** {issue['message']}")
                st.markdown(f"**Evidence:** {issue['evidence']}")
                st.markdown(f"**Recommendation:** {issue['recommendation']}")
    
    # SECTION 3: LEAKAGE DETECTION
    st.markdown("## ⚠️ Leakage Detection")
    
    leakage = results['leakage']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Candidates", leakage['total_candidates'])
    
    with col2:
        st.metric("High Risk", leakage['high_risk'])
    
    with col3:
        st.metric("Medium Risk", leakage['medium_risk'])
    
    if leakage['candidates']:
        st.markdown("### Leakage Candidates")
        
        for candidate in leakage['candidates'][:10]:  # Top 10
            confidence = candidate.get('confidence', 0)
            feature = candidate.get('feature', 'unknown')
            message = candidate.get('message', '')
            
            icon = "🔴" if confidence > 0.8 else "🟠" if confidence > 0.5 else "🟡"
            
            with st.expander(f"{icon} {feature} ({confidence*100:.0f}% confidence)"):
                st.markdown(f"**Issue:** {message}")
                st.markdown(f"**Recommendation:** {candidate.get('recommendation', 'Review manually')}")
    
    # SECTION 4: TARGET ANALYSIS
    st.markdown("## 🎲 Target Variable Analysis")
    
    target = results['target']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Type:** {target['type'].title()}  
        **Unique Values:** {target['n_unique']}  
        **Missing:** {target['n_missing']} ({target['pct_missing']:.1f}%)
        """)
    
    with col2:
        if target['type'] == 'classification':
            st.markdown(f"""
            **Classes:** {len(target.get('classes', []))}  
            **Imbalanced:** {'Yes' if not target.get('is_balanced', True) else 'No'}  
            **Min Class:** {target.get('min_class_percentage', 0):.1f}%
            """)
    
    # SECTION 5: RECOMMENDATIONS
    st.markdown("## ✅ Recommended Actions")
    
    recommendations = []
    
    # Collect from data quality
    for issue in quality['issues']:
        if issue['severity'] in ['HIGH', 'MEDIUM']:
            recommendations.append({
                'severity': issue['severity'],
                'issue': issue['message'],
                'action': issue['recommendation']
            })
    
    # Collect from leakage
    for candidate in leakage['candidates']:
        if candidate.get('confidence', 0) > 0.5:
            recommendations.append({
                'severity': 'HIGH' if candidate.get('confidence', 0) > 0.8 else 'MEDIUM',
                'issue': candidate.get('message', ''),
                'action': candidate.get('recommendation', '')
            })
    
    # Sort by severity
    severity_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    recommendations.sort(key=lambda x: severity_order.get(x['severity'], 3))
    
    for i, rec in enumerate(recommendations[:5], 1):  # Top 5
        severity = rec['severity']
        icon = "🔴" if severity == "HIGH" else "🟠"
        
        st.markdown(f"{i}. {icon} **{rec['issue']}**")
        st.markdown(f"   → {rec['action']}")


def main():
    """Main app."""
    create_sidebar()
    
    # Title
    st.markdown("""
    # 🛡️ ModelGuard AI
    **An AI Second Opinion System for Machine Learning Models**
    """)
    
    st.markdown("Detect data leakage, validation errors, and methodological risks in your ML projects.")
    st.markdown("---")
    
    # Main workflow
    tab1, tab2, tab3 = st.tabs(["📁 Upload", "🔍 Analyze", "📊 Results"])
    
    with tab1:
        if upload_data_section():
            data_preview_section()
    
    with tab2:
        if st.session_state.df is not None:
            if st.button("▶️ Run Audit", use_container_width=True, type="primary"):
                run_audit()
    
    with tab3:
        if st.session_state.audit_results:
            display_results()
            
            # Export button
            st.markdown("---")
            st.markdown("### 📥 Export Report")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📄 Download JSON Report"):
                    report_gen = ReportGenerator()
                    report = report_gen.generate(st.session_state.audit_results)
                    
                    import json
                    json_str = json.dumps(report, indent=2, default=str)
                    
                    st.download_button(
                        label="Click to download JSON",
                        data=json_str,
                        file_name="modelguard_report.json",
                        mime="application/json"
                    )
            
            with col2:
                if st.button("📝 Download Text Report"):
                    report_gen = ReportGenerator()
                    report = report_gen.generate(st.session_state.audit_results)
                    
                    text_output = report_gen.format_for_display(report)
                    
                    st.download_button(
                        label="Click to download TXT",
                        data=text_output,
                        file_name="modelguard_report.txt",
                        mime="text/plain"
                    )
        else:
            st.info("👈 Upload data and run audit to see results")


if __name__ == "__main__":
    main()

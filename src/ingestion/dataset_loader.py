"""
Dataset Loader Module

Loads datasets from various formats (CSV, Excel, JSON, Parquet).
Handles data type inference and basic validation.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, Tuple, Optional
import io


class DatasetLoader:
    """Load and validate datasets from various file formats."""
    
    SUPPORTED_FORMATS = ['.csv', '.xlsx', '.json', '.parquet', '.xls']
    
    @staticmethod
    def load_dataset(file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """
        Load a dataset from file.
        
        Args:
            file_path: Path to the dataset file
            **kwargs: Additional arguments for pandas read functions
            
        Returns:
            Pandas DataFrame
            
        Raises:
            ValueError: If file format not supported
            FileNotFoundError: If file doesn't exist
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = file_path.suffix.lower()
        
        if suffix not in DatasetLoader.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: {suffix}. "
                f"Supported: {', '.join(DatasetLoader.SUPPORTED_FORMATS)}"
            )
        
        try:
            if suffix == '.csv':
                return pd.read_csv(file_path, **kwargs)
            elif suffix in ['.xlsx', '.xls']:
                return pd.read_excel(file_path, **kwargs)
            elif suffix == '.json':
                return pd.read_json(file_path, **kwargs)
            elif suffix == '.parquet':
                return pd.read_parquet(file_path, **kwargs)
        except Exception as e:
            raise ValueError(f"Error reading file {file_path}: {str(e)}")
    
    @staticmethod
    def load_from_bytes(file_bytes: bytes, file_extension: str, **kwargs) -> pd.DataFrame:
        """
        Load dataset from bytes (useful for web uploads).
        
        Args:
            file_bytes: File content as bytes
            file_extension: File extension (e.g., '.csv', '.xlsx')
            **kwargs: Additional arguments for pandas read functions
            
        Returns:
            Pandas DataFrame
        """
        file_extension = file_extension.lower()
        
        if file_extension not in DatasetLoader.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: {file_extension}. "
                f"Supported: {', '.join(DatasetLoader.SUPPORTED_FORMATS)}"
            )
        
        try:
            if file_extension == '.csv':
                return pd.read_csv(io.BytesIO(file_bytes), **kwargs)
            elif file_extension in ['.xlsx', '.xls']:
                return pd.read_excel(io.BytesIO(file_bytes), **kwargs)
            elif file_extension == '.json':
                return pd.read_json(io.BytesIO(file_bytes), **kwargs)
            elif file_extension == '.parquet':
                return pd.read_parquet(io.BytesIO(file_bytes), **kwargs)
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")
    
    @staticmethod
    def load_with_target(
        file_path: Union[str, Path],
        target_column: str,
        **kwargs
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load dataset and separate target variable.
        
        Args:
            file_path: Path to dataset
            target_column: Name of target column
            **kwargs: Additional arguments for pandas read functions
            
        Returns:
            Tuple of (features DataFrame, target Series)
            
        Raises:
            ValueError: If target column not found
        """
        df = DatasetLoader.load_dataset(file_path, **kwargs)
        
        if target_column not in df.columns:
            raise ValueError(
                f"Target column '{target_column}' not found in dataset. "
                f"Available columns: {list(df.columns)}"
            )
        
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        return X, y
    
    @staticmethod
    def validate_data(df: pd.DataFrame) -> dict:
        """
        Perform basic validation on loaded data.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary with validation results
        """
        issues = []
        
        # Check if empty
        if df.empty:
            issues.append("Dataset is empty")
        
        # Check column names
        if not df.columns.is_unique:
            issues.append("Dataset has duplicate column names")
        
        # Check for all NaN columns
        all_nan_cols = df.columns[df.isnull().all()].tolist()
        if all_nan_cols:
            issues.append(f"Columns with all missing values: {', '.join(all_nan_cols)}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict()
        }
    
    @staticmethod
    def infer_target_type(y: pd.Series) -> str:
        """
        Infer whether target is classification or regression.
        
        Args:
            y: Target series
            
        Returns:
            'classification' or 'regression'
        """
        # Check if numeric
        if pd.api.types.is_numeric_dtype(y):
            # If small number of unique values, likely classification
            n_unique = y.nunique()
            n_total = len(y)
            
            # If categorical-looking (few unique values relative to total)
            if n_unique <= 20 and n_unique / n_total < 0.1:
                return 'classification'
            else:
                return 'regression'
        else:
            return 'classification'
    
    @staticmethod
    def get_dataset_info(df: pd.DataFrame) -> dict:
        """
        Get comprehensive information about dataset.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with dataset information
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        return {
            'shape': df.shape,
            'n_rows': len(df),
            'n_columns': len(df.columns),
            'numeric_columns': numeric_cols,
            'categorical_columns': categorical_cols,
            'datetime_columns': df.select_dtypes(include=['datetime64']).columns.tolist(),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
            'missing_values_total': df.isnull().sum().sum(),
            'duplicate_rows': df.duplicated().sum(),
            'column_names': list(df.columns),
            'dtypes': df.dtypes.to_dict()
        }

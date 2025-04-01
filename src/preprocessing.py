import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pickle
from typing import Tuple, Optional, Dict

# Define feature columns
NUMERIC_COLUMNS = [
    'Mother_Education', 'Father_Education', 'Final_Grade', 'Grade_1',
    'Grade_2', 'Number_of_Failures', 'Study_Time',
    'Weekend_Alcohol_Consumption', 'Weekday_Alcohol_Consumption'
]

CATEGORICAL_COLUMNS = [
    'School', 'Wants_Higher_Education', 'Address', 'Reason_for_Choosing_School'
]

ALL_FEATURES = NUMERIC_COLUMNS + CATEGORICAL_COLUMNS
TARGET_COLUMN = 'Dropped_Out'

def create_category_mapping(df: pd.DataFrame, categorical_columns: list) -> Dict[str, str]:
    """
    Creates a mapping from categorical feature values to one-hot encoded column names.
    
    Args:
        df: DataFrame with categorical columns.
        categorical_columns: List of categorical column names.
    
    Returns:
        Dictionary mapping 'column_value' to 'column_value'.
    """
    category_mapping = {}
    for column in categorical_columns:
        unique_values = df[column].unique()
        for value in unique_values:
            one_hot_column_name = f"{column}_{value}"
            category_mapping[f"{column}_{value}"] = one_hot_column_name
    return category_mapping

def create_preprocessor() -> Pipeline:
    """
    Creates a preprocessing pipeline with standard scaling and one-hot encoding.
    
    Returns:
        Pipeline: A preprocessing pipeline.
    """
    # Numeric transformer: impute missing values only (scaling applied later)
    numeric_transformer = SimpleImputer(strategy='mean')
    
    # Categorical transformer: impute and one-hot encode
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
    ])
    
    # Combine transformers into a ColumnTransformer
    column_transformer = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERIC_COLUMNS),
            ('cat', categorical_transformer, CATEGORICAL_COLUMNS)
        ]
    )
    
    # Full pipeline: apply column transformations, then scale all features
    preprocessor = Pipeline(steps=[
        ('column_transformer', column_transformer),
        ('scaler', StandardScaler())
    ])
    
    return preprocessor

def preprocess_training_data(df: pd.DataFrame, preprocessor_path: str, mapping_path: str) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    """
    Preprocesses training data, saves the fitted preprocessor and category mapping.
    
    Args:
        df: DataFrame with features and target.
        preprocessor_path: Path to save the fitted preprocessor.
        mapping_path: Path to save the category mapping.
    
    Returns:
        Tuple of processed features (X) and target (y).
    
    Raises:
        ValueError: If data is empty, missing required columns, or has incorrect number of columns.
    """
    if df.empty:
        raise ValueError("Training data is empty.")
    
    required_columns = set(ALL_FEATURES + [TARGET_COLUMN])
    if not required_columns.issubset(df.columns):
        missing_cols = required_columns - set(df.columns)
        raise ValueError(f"Missing columns: {missing_cols}")
    
    if len(df.columns) != len(required_columns):
        raise ValueError(f"Expected {len(required_columns)} columns, got {len(df.columns)}.")
    
    # Create and save category mapping (as in your notebook)
    category_mapping = create_category_mapping(df, CATEGORICAL_COLUMNS)
    with open(mapping_path, 'wb') as file:
        pickle.dump(category_mapping, file)
    
    # Drop rows with missing target
    df = df.dropna(subset=[TARGET_COLUMN])
    if df.empty:
        raise ValueError("No training data after dropping rows with missing targets.")
    
    # Separate features and target
    X = df[ALL_FEATURES]
    y = df[TARGET_COLUMN]
    
    # Create and fit preprocessor
    preprocessor = create_preprocessor()
    X_processed = preprocessor.fit_transform(X)
    
    # Save the fitted preprocessor (includes StandardScaler)
    with open(preprocessor_path, 'wb') as file:
        pickle.dump(preprocessor, file)
    
    return X_processed, y.to_numpy()

def preprocess_prediction_data(df: pd.DataFrame, preprocessor_path: str) -> Optional[np.ndarray]:
    """
    Preprocesses prediction/test data using a saved preprocessor.
    
    Args:
        df: DataFrame with features only.
        preprocessor_path: Path to the saved preprocessor.
    
    Returns:
        Processed features (X).
    
    Raises:
        ValueError: If data is empty, missing required columns, or has incorrect number of columns.
    """
    if df.empty:
        raise ValueError("Prediction data is empty.")
    
    required_columns = set(ALL_FEATURES)
    if not required_columns.issubset(df.columns):
        missing_cols = required_columns - set(df.columns)
        raise ValueError(f"Missing columns: {missing_cols}")
    
    if len(df.columns) != len(required_columns):
        raise ValueError(f"Expected {len(required_columns)} columns, got {len(df.columns)}.")
    
    # Load the saved preprocessor (includes StandardScaler from training)
    with open(preprocessor_path, 'rb') as file:
        preprocessor = pickle.load(file)
    
    # Transform features
    X_processed = preprocessor.transform(df)
    
    return X_processed

def preprocess_single_input(input_row: Dict, preprocessor_path: str, mapping_path: str = None, use_mapping: bool = False) -> np.ndarray:
    """
    Preprocesses a single input row for prediction.
    
    Args:
        input_row: Dictionary with feature names and values.
        preprocessor_path: Path to the saved preprocessor.
        mapping_path: Path to the saved category mapping (required if use_mapping=True).
        use_mapping: If True, use category_mapping and map_input_row; otherwise, use pipeline.
    
    Returns:
        Processed features as a numpy array.
    
    Raises:
        ValueError: If input is missing required features or mapping_path is missing when needed.
    """
    required_features = set(ALL_FEATURES)
    if not required_features.issubset(input_row.keys()):
        missing_features = required_features - set(input_row.keys())
        raise ValueError(f"Missing features in input: {missing_features}")
    
    if use_mapping:
        if not mapping_path:
            raise ValueError("mapping_path must be provided when use_mapping=True")
        
        # Load category mapping
        with open(mapping_path, 'rb') as file:
            category_mapping = pickle.load(file)
        
        # Map input row to one-hot encoded format
        encoded_series = map_input_row(input_row, category_mapping)
        
        # Include numeric features
        numeric_values = pd.Series({col: input_row[col] for col in NUMERIC_COLUMNS})
        full_input = pd.concat([numeric_values, encoded_series], axis=0)
        
        # Load preprocessor to get scaler
        with open(preprocessor_path, 'rb') as file:
            preprocessor = pickle.load(file)
        
        # Get expected feature names from training
        feature_names = preprocessor.named_steps['column_transformer'].get_feature_names_out()
        full_input = full_input.reindex(feature_names, fill_value=0)
        
        # Scale the input
        X_processed = preprocessor.named_steps['scaler'].transform(full_input.values.reshape(1, -1))
        
    else:
        # Convert input row to DataFrame and use pipeline
        input_df = pd.DataFrame([input_row])
        X_processed = preprocess_prediction_data(input_df, preprocessor_path)
    
    return X_processed

def map_input_row(input_row: Dict, category_mapping: Dict[str, str]) -> pd.Series:
    """
    Maps a row of input features to one-hot encoded values using category_mapping.
    
    Args:
        input_row: Dictionary representing a row of input features.
        category_mapping: Dictionary containing the mapping.
    
    Returns:
        Pandas Series with one-hot encoded values.
    """
    encoded_values = pd.Series(0, index=category_mapping.values())
    
    for feature_name, feature_value in input_row.items():
        if feature_name in set([k.split('_')[0] for k in category_mapping]):
            one_hot_column_name = category_mapping.get(f"{feature_name}_{feature_value}")
            if one_hot_column_name:
                encoded_values[one_hot_column_name] = 1
            else:
                print(f"Warning: No mapping found for {feature_name}: {feature_value}")
    
    return encoded_values
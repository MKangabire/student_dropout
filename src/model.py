import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.callbacks import EarlyStopping
from typing import Dict, Optional


def retrain_model(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, model_path: str) -> Optional['Sequential']:
    """
    Loads an existing Keras model, retrains it, and saves the updated model.

    Args:
        X_train: Training feature matrix.
        y_train: Training target array.
        X_val: Validation feature matrix.
        y_val: Validation target array.
        model_path: Path to the existing and updated model file (e.g., 'models/model.keras').

    Returns:
        Retrained Keras model, or None if retraining fails.

    Raises:
        ValueError: If X_train, y_train, X_val, or y_val is empty or shapes don’t match.
        FileNotFoundError: If the model file doesn’t exist at model_path.
    """
    # Input validation
    if X_train.size == 0 or y_train.size == 0 or X_val.size == 0 or y_val.size == 0:
        raise ValueError("Feature matrix or target array is empty.")
    
    if X_train.shape[0] != y_train.shape[0] or X_val.shape[0] != y_val.shape[0]:
        raise ValueError("Number of samples in X and y do not match for training or validation.")

    # Load the existing model
    try:
        model = load_model(model_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at {model_path}. Please ensure the pre-trained model exists.")

    # Define early stopping to prevent overfitting
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    # Retrain the model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=400,
        verbose=2,
        callbacks=[early_stopping]
    )

    # Save the retrained model
    model.save(model_path)
    return model

def evaluate_model(model_path: str, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
    """
    Evaluates the model on test data and returns metrics and predictions.

    Args:
        model_path: Path to the saved model (e.g., 'models/model.keras').
        X_test: Test feature matrix.
        y_test: Test target array.

    Returns:
        A dictionary containing:
            - 'classification_report': Classification report as a dictionary with precision, recall, F1-score, and accuracy.
            - 'confusion_matrix': Confusion matrix as a list of lists.
            - 'y_pred': Predicted values as a list.
            - 'y_test': Actual target values as a list.

    Raises:
        ValueError: If X_test or y_test is empty.
        FileNotFoundError: If the model file doesn’t exist at model_path.
    """
    # Check if inputs are valid
    if X_test.size == 0 or y_test.size == 0:
        raise ValueError("Test feature matrix or target array is empty.")

    # Load the model from the provided path
    try:
        model = load_model(model_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at {model_path}. Please ensure the model exists.")

    # Make predictions (assuming binary classification with a 0.5 threshold)
    y_pred = (model.predict(X_test) > 0.5).astype("int32")

    # Compute the classification report as a dictionary
    report_dict = classification_report(y_test, y_pred, output_dict=True)

    # Compute the confusion matrix
    cm = confusion_matrix(y_test, y_pred).tolist()

    # Convert predictions and actual values to lists for serialization
    y_pred_list = y_pred.flatten().tolist()
    y_test_list = y_test.flatten().tolist()

    # Return all required data in a dictionary
    return {
        'classification_report': report_dict,
        'confusion_matrix': cm,
        'y_pred': y_pred_list,
        'y_test': y_test_list
    }
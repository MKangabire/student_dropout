import numpy as np
from tensorflow.keras.models import load_model
from typing import Optional

def make_predictions(X: np.ndarray, model_path: str) -> Optional[np.ndarray]:
    """
    Makes predictions using a retrained Keras neural network model.

    Args:
        X: Processed feature matrix.
        model_path: Path to the retrained model (e.g., 'models/model.keras').

    Returns:
        Array of binary predictions, or None if prediction fails.

    Raises:
        ValueError: If X is empty.
        FileNotFoundError: If the model file doesn’t exist at model_path.
    """
    if X.size == 0:
        raise ValueError("Feature matrix is empty.")

    # Load the retrained model
    try:
        model = load_model(model_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at {model_path}. Please ensure the retrained model exists.")

    # Make predictions
    predictions = (model.predict(X) > 0.5).astype("int32")
    return predictions
import pandas as pd
from sklearn.model_selection import train_test_split
from src.preprocessing import preprocess_training_data, preprocess_prediction_data
from src.model import retrain_model, evaluate_model
from src.prediction import make_predictions

columns_to_keep = [
    'Dropped_Out', 'Mother_Education', 'Father_Education', 'Final_Grade', 'Grade_1',
    'Grade_2', 'Number_of_Failures', 'School', 'Wants_Higher_Education', 'Study_Time', 
    'Weekend_Alcohol_Consumption', 'Weekday_Alcohol_Consumption', 'Address',
    'Reason_for_Choosing_School'

]

# Define paths for saved artifacts (based on your models/ folder)
preprocessor_path = "models/preprocessor.pkl"
mapping_path = "models/category_mapping.pkl"
model_path = "models/model.keras"

# Load train and test data
train_df = pd.read_csv("data/train/train.csv")
test_df = pd.read_csv("data/test/test.csv")


train_df = train_df[columns_to_keep]
test_df = test_df[columns_to_keep]

X_train_full, y_train_full = preprocess_training_data(train_df, preprocessor_path, mapping_path)
print("Training data preprocessed successfully.")

# Split training data into train and validation sets for retraining
X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, 
    y_train_full, 
    test_size=0.2,  # 20% for validation
    random_state=42
)
print(f"Training set shape: {X_train.shape}, Validation set shape: {X_val.shape}")

# Retrain the model using train and validation data
retrain_model(X_train, y_train, X_val, y_val, model_path)
print("Model retrained and saved successfully.")

feature_columns = [
    'Mother_Education', 'Father_Education', 'Final_Grade', 'Grade_1',
    'Grade_2', 'Number_of_Failures', 'Study_Time',
    'Weekend_Alcohol_Consumption', 'Weekday_Alcohol_Consumption',
    'School', 'Wants_Higher_Education', 'Address', 'Reason_for_Choosing_School'
]
X_test = preprocess_prediction_data(test_df[feature_columns], preprocessor_path)
y_test = test_df['Dropped_Out'].to_numpy()  # Assuming 'Dropped_Out' is the target column
print("Test data preprocessed successfully.")

# Evaluate the model
metrics = evaluate_model(model_path, X_test, y_test)
print("Evaluation metrics:", metrics)

# Make predictions on a sample row
sample_row = test_df[feature_columns].iloc[0:1]  # Take the first row, only features
X_sample = preprocess_prediction_data(sample_row, preprocessor_path)
prediction = make_predictions(X_sample, model_path)
print("Sample prediction:", prediction)

print("Pipeline test completed successfully.")
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Added CORS import
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import io
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from typing import Dict
from .database import save_to_mongo, fetch_from_mongo  # Relative import
from ..preprocessing import preprocess_training_data, preprocess_prediction_data  # Relative import
from ..model import retrain_model, evaluate_model  # Relative import
from ..prediction import make_predictions  # Relative import

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://studentdropout-qugy2gmua-mkangabires-projects.vercel.app"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define the expected 34 columns for upload
ALL_COLUMNS = [
    'School', 'Gender', 'Age', 'Address', 'Family_Size', 'Parental_Status',
    'Mother_Education', 'Father_Education', 'Mother_Job', 'Father_Job',
    'Reason_for_Choosing_School', 'Guardian', 'Travel_Time', 'Study_Time',
    'Number_of_Failures', 'School_Support', 'Family_Support',
    'Extra_Paid_Class', 'Extra_Curricular_Activities', 'Attended_Nursery',
    'Wants_Higher_Education', 'Internet_Access', 'In_Relationship',
    'Family_Relationship', 'Free_Time', 'Going_Out',
    'Weekend_Alcohol_Consumption', 'Weekday_Alcohol_Consumption',
    'Health_Status', 'Number_of_Absences', 'Grade_1', 'Grade_2',
    'Final_Grade', 'Dropped_Out'
]

# Define the 14 columns for preprocessing
COLUMNS_TO_KEEP = [
    'Dropped_Out', 'Mother_Education', 'Father_Education', 'Final_Grade', 'Grade_1',
    'Grade_2', 'Number_of_Failures', 'School', 'Wants_Higher_Education', 'Study_Time',
    'Weekend_Alcohol_Consumption', 'Weekday_Alcohol_Consumption', 'Address',
    'Reason_for_Choosing_School'
]

# Define directories and model paths (relative to project root)
TRAIN_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "train")
TEST_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "test")
PREPROCESSOR_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "preprocessor.pkl")
MAPPING_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "category_mapping.pkl")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "model.keras")
os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(TEST_DIR, exist_ok=True)

# Existing /upload_train_data endpoint
@app.post("/upload_train_data")
async def upload_train_data(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV.")
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded CSV is empty.")
        if len(df.columns) != 34 or list(df.columns) != ALL_COLUMNS:
            missing = set(ALL_COLUMNS) - set(df.columns)
            extra = set(df.columns) - set(ALL_COLUMNS)
            error_msg = "CSV must have exactly 34 columns matching the expected names."
            if missing:
                error_msg += f" Missing: {', '.join(missing)}."
            if extra:
                error_msg += f" Extra: {', '.join(extra)}."
            raise HTTPException(status_code=400, detail=error_msg)
        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
        save_to_mongo(train_df, "train")
        save_to_mongo(test_df, "test")
        train_path = os.path.join(TRAIN_DIR, "train.csv")
        test_path = os.path.join(TEST_DIR, "test.csv")
        train_df.to_csv(train_path, index=False)
        test_df.to_csv(test_path, index=False)
        return JSONResponse(
            content={
                "message": "Training data uploaded, split, and saved successfully.",
                "train_records": len(train_df),
                "test_records": len(test_df),
                "mongo_collections": ["train", "test"],
                "backup_paths": {"train": train_path, "test": test_path}
            }
        )
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Uploaded CSV is empty or malformed.")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Error parsing CSV file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Retrain endpoint
@app.post("/retrain")
async def retrain():
    """
    Retrains the model using data from MongoDB or backup files.
    
    Returns:
        JSON response with success message or error details.
    """
    try:
        train_df = fetch_from_mongo("train")
        if train_df is None:
            train_path = os.path.join(TRAIN_DIR, "train.csv")
            if not os.path.exists(train_path):
                raise HTTPException(status_code=404, detail="No training data available.")
            train_df = pd.read_csv(train_path)
        train_df = train_df[COLUMNS_TO_KEEP]
        X_train_full, y_train_full = preprocess_training_data(train_df, PREPROCESSOR_PATH, MAPPING_PATH)
        X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=0.2, random_state=42)
        retrain_model(X_train, y_train, X_val, y_val, MODEL_PATH)
        return JSONResponse(content={"message": "Model retrained successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during retraining: {str(e)}")

# Predict endpoint (single datapoint)
@app.post("/predict")
async def predict(
    School: str = Form(...),
    Mother_Education: int = Form(...),
    Father_Education: int = Form(...),
    Final_Grade: int = Form(...),
    Grade_1: int = Form(...),
    Grade_2: int = Form(...),
    Number_of_Failures: int = Form(...),
    Wants_Higher_Education: str = Form(...),
    Study_Time: int = Form(...),
    Weekend_Alcohol_Consumption: int = Form(...),
    Weekday_Alcohol_Consumption: int = Form(...),
    Address: str = Form(...),
    Reason_for_Choosing_School: str = Form(...)
):
    """
    Makes a prediction for a single datapoint provided via form data.
    
    Args:
        Feature values as form inputs (13 features required by preprocessing).
    
    Returns:
        JSON response with the prediction.
    """
    try:
        input_data = {
            "School": School,
            "Mother_Education": Mother_Education,
            "Father_Education": Father_Education,
            "Final_Grade": Final_Grade,
            "Grade_1": Grade_1,
            "Grade_2": Grade_2,
            "Number_of_Failures": Number_of_Failures,
            "Wants_Higher_Education": Wants_Higher_Education,
            "Study_Time": Study_Time,
            "Weekend_Alcohol_Consumption": Weekend_Alcohol_Consumption,
            "Weekday_Alcohol_Consumption": Weekday_Alcohol_Consumption,
            "Address": Address,
            "Reason_for_Choosing_School": Reason_for_Choosing_School
        }
        input_df = pd.DataFrame([input_data])
        X_processed = preprocess_prediction_data(input_df, PREPROCESSOR_PATH)
        prediction = make_predictions(X_processed, MODEL_PATH)
        return JSONResponse(content={"prediction": int(prediction[0])})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

# Evaluate endpoint
@app.post("/evaluate")
async def evaluate():
    """
    Evaluates the model using test data from MongoDB or backup files.
    
    Returns:
        JSON response with evaluation metrics.
    """
    try:
        test_df = fetch_from_mongo("test")
        if test_df is None:
            test_path = os.path.join(TEST_DIR, "test.csv")
            if not os.path.exists(test_path):
                raise HTTPException(status_code=404, detail="No test data available.")
            test_df = pd.read_csv(test_path)
        test_df = test_df[COLUMNS_TO_KEEP]
        X_test = preprocess_prediction_data(test_df.drop(columns=['Dropped_Out']), PREPROCESSOR_PATH)
        y_test = test_df['Dropped_Out'].to_numpy()
        metrics = evaluate_model(MODEL_PATH, X_test, y_test)
        return JSONResponse(content=metrics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during evaluation: {str(e)}")

# Visualize endpoint
@app.get("/visualize/{feature_name}")
async def visualize_feature(feature_name: str):
    """
    Generates a visualization for the specified feature and provides an interpretation.
    
    Args:
        feature_name (str): The name of the feature to visualize (e.g., 'Grade_1', 'Study_Time', 'Number_of_Failures').
    
    Returns:
        JSONResponse: Contains the base64-encoded image of the plot and an interpretation text.
    
    Raises:
        HTTPException: If the feature is invalid or data cannot be fetched.
    """
    valid_features = ['Grade_1', 'Study_Time', 'Number_of_Failures']
    if feature_name not in valid_features:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid feature name. Choose from: {', '.join(valid_features)}."
        )
    try:
        df = fetch_from_mongo("train")
        if df is None:
            train_path = os.path.join(TRAIN_DIR, "train.csv")
            if not os.path.exists(train_path):
                raise HTTPException(status_code=404, detail="No training data available.")
            df = pd.read_csv(train_path)
        df = df[COLUMNS_TO_KEEP]
        plt.figure(figsize=(10, 6))
        if feature_name == "Grade_1":
            sns.kdeplot(data=df, x="Grade_1", hue="Dropped_Out", fill=True)
            plt.title("Distribution of Grade_1 by Dropout Status")
            plt.xlabel("First-Year Grade")
            plt.ylabel("Density")
            interpretation = (
                "The distribution of first-year grades shows that students who dropped out tend to have lower grades "
                "compared to those who did not. This suggests that academic performance in the first year is a strong "
                "indicator of dropout risk."
            )
        elif feature_name == "Study_Time":
            sns.boxplot(data=df, x="Dropped_Out", y="Study_Time")
            plt.title("Study Time by Dropout Status")
            plt.xlabel("Dropped Out (0 = No, 1 = Yes)")
            plt.ylabel("Study Time")
            interpretation = (
                "The box plot indicates that students who dropped out generally reported less study time than those who stayed."
            )
        elif feature_name == "Number_of_Failures":
            failure_counts = df.groupby("Number_of_Failures")["Dropped_Out"].mean()
            sns.barplot(x=failure_counts.index, y=failure_counts.values)
            plt.title("Proportion of Dropouts by Number of Failures")
            plt.xlabel("Number of Failures")
            plt.ylabel("Proportion Dropped Out")
            interpretation = (
                "As the number of failures increases, the proportion of students who drop out rises."
            )
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return JSONResponse(content={"image": img_base64, "interpretation": interpretation})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating visualization: {str(e)}")
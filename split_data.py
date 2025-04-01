import pandas as pd
from sklearn.model_selection import train_test_split
import os

def split_and_save_data(csv_path, train_path, test_path, test_size=0.2, random_state=42):
    """
    Splits the dataset into train and test sets and saves them to specified paths.

    Args:
        csv_path (str): Path to the input CSV file.
        train_path (str): Path to save the training set.
        test_path (str): Path to save the testing set.
        test_size (float): Proportion of the dataset to include in the test split (default: 0.2).
        random_state (int): Seed for random number generator for reproducibility (default: 42).
    """
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Split the data into train and test sets
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
    
    # Ensure the output directories exist
    os.makedirs(os.path.dirname(train_path), exist_ok=True)
    os.makedirs(os.path.dirname(test_path), exist_ok=True)
    
    # Save the splits to CSV files
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f"Train data saved to {train_path}")
    print(f"Test data saved to {test_path}")

if __name__ == "__main__":
    # Define file paths based on the directory structure
    csv_path = "dataset/student dropout.csv"
    train_path = "data/train/train.csv"
    test_path = "data/test/test.csv"
    
    # Execute the splitting function
    split_and_save_data(csv_path, train_path, test_path)
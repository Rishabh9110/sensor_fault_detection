import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import pickle
import os

def train_sensor_model():
    print("🚀 Loading dataset from 'data' folder...")
    # Dataset path updated based on your project structure
    try:
        file_path = 'data/aps_failure_training_set.csv'
        df = pd.read_csv(file_path, na_values="na")
    except FileNotFoundError:
        print(f"❌ Error: '{file_path}' nahi mili. Check karein ki file 'data' folder mein hai.")
        return

    # 1. Preprocessing
    print("🛠️ Preprocessing data...")
    if 'class' in df.columns:
        df['class'] = df['class'].map({'neg': 0, 'pos': 1})
        X = df.drop('class', axis=1)
        y = df['class']
    else:
        print("❌ Error: Dataset mein 'class' column nahi mila.")
        return

    # Handling missing values (Imputation)
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)
    X_final = pd.DataFrame(X_imputed, columns=X.columns)

    # 2. Model Training
    print("🧠 Training Random Forest Model... (Please wait)")
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_final, y)

    # 3. Saving the Model
    with open('sensor_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("✅ Success! 'sensor_model.pkl' root folder mein create ho gayi hai.")

if __name__ == "__main__":
    train_sensor_model()
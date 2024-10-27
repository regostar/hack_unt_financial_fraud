import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import os

# Use the absolute path to load the dataset
file_path = r'E:\Masters Of Computer Science\Hackathon2024\Dataset\datasets\teamincribo\credit-card-fraud\versions\5\credit_card_fraud.csv'
df = pd.read_csv(file_path)

print("Original Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())
print("\nSample data:")
print(df.head())

# Handle missing values
def handle_missing_values(df):
    print("\nMissing values before handling:")
    print(df.isnull().sum())

    for column in df.columns:
        if df[column].dtype in ['float64', 'int64']:
            df[column] = df[column].fillna(df[column].mean())
        else:
            df[column] = df[column].fillna(df[column].mode()[0])

    print("\nMissing values after handling:")
    print(df.isnull().sum())
    return df

df = handle_missing_values(df)

# Preprocess 'Previous Transactions' column
def preprocess_previous_transactions(value):
    if pd.isna(value):
        return 0
    elif value == '3 or more':
        return 3
    else:
        return float(value)

df['Previous Transactions'] = df['Previous Transactions'].apply(preprocess_previous_transactions)

# Encode categorical variables
categorical_columns = ['Cardholder Name', 'Merchant Name', 'Transaction Location (City or ZIP Code)',
                       'Transaction Currency', 'Card Type', 'Transaction Source', 'Device Information',
                       'User Account Information']

df_encoded = pd.get_dummies(df, columns=categorical_columns)

print("\nEncoded Dataset shape:", df_encoded.shape)

# Scale numerical features
numerical_cols = ['Transaction Amount', 'Merchant Category Code (MCC)', 'Previous Transactions']
scaler = StandardScaler()
df_encoded[numerical_cols] = scaler.fit_transform(df_encoded[numerical_cols])

# Prepare features and target
X = df_encoded.drop(['Fraud Flag or Label', 'Transaction Date and Time', 'Card Number (Hashed or Encrypted)',
                     'CVV Code (Hashed or Encrypted)', 'Transaction ID', 'IP Address', 'Transaction Notes'], axis=1)
y = df_encoded['Fraud Flag or Label']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\nFinal preprocessed data shapes:")
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)

# Save preprocessed data (optional)
# Make sure to create the directory structure if it doesn’t exist
output_dir = r'E:\Masters Of Computer Science\Hackathon2024\Dataset\data\preprocess'
os.makedirs(output_dir, exist_ok=True)

X_train.to_csv(os.path.join(output_dir, 'X_train_preprocessed.csv'), index=False)
X_test.to_csv(os.path.join(output_dir, 'X_test_preprocessed.csv'), index=False)
y_train.to_csv(os.path.join(output_dir, 'y_train_preprocessed.csv'), index=False)
y_test.to_csv(os.path.join(output_dir, 'y_test_preprocessed.csv'), index=False)

print("\nPreprocessing completed. Preprocessed data saved to CSV files.")

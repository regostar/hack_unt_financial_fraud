import pandas as pd
import torch
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load the new dataset

file_path = r'E:\Masters Of Computer Science\Hackathon2024\Dataset\datasets\teamincribo\credit-card-fraud\versions\5\credit_card_fraud.csv'
df = pd.read_csv(file_path)
new_test_data = df.head(100)

# Load the saved model and tokenizer
model_path = r'E:\Masters Of Computer Science\Hackathon2024\model\llm\llama_fraud_detection_model'
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Prepare the data for the model
def prepare_data_for_llama(X):
    return X.apply(lambda row: f"Transaction: {' '.join(map(str, row))}", axis=1).tolist()

test_data_prepared = prepare_data_for_llama(new_test_data)

# Tokenize the data
encodings = tokenizer(test_data_prepared, truncation=True, padding=True, max_length=512, return_tensors="pt")

# Set device
device = torch.device("cpu")
model.to(device)

# Make predictions
model.eval()
with torch.no_grad():
    input_ids = encodings['input_ids'].to(device)
    attention_mask = encodings['attention_mask'].to(device)
    outputs = model(input_ids=input_ids, attention_mask=attention_mask)
    
    # Apply softmax to get probabilities
    probabilities = F.softmax(outputs.logits, dim=-1)
    
    # Get the probability of fraud (assuming fraud is label 1)
    fraud_probabilities = probabilities[:, 1].cpu().numpy()

# Set a very low threshold for fraud detection (e.g., 0.001 or 0.1%)
FRAUD_THRESHOLD = 0.001

# Add predictions and fraud probabilities to the dataframe
new_test_data['Fraud_Probability'] = fraud_probabilities
new_test_data['Predicted_Fraud'] = new_test_data['Fraud_Probability'] > FRAUD_THRESHOLD

# Filter and display suspicious transactions
suspicious_transactions = new_test_data[new_test_data['Predicted_Fraud']]

print("Suspicious Transactions:")
for index, transaction in suspicious_transactions.iterrows():
    print(f"Transaction {index}:")
    for column, value in transaction.items():
        if column not in ['Predicted_Fraud', 'Fraud_Probability']:
            print(f"  {column}: {value}")
    print(f"  Fraud Probability: {transaction['Fraud_Probability']:.6f}")
    print()

print(f"Total number of transactions: {len(new_test_data)}")
print(f"Number of suspicious transactions: {len(suspicious_transactions)}")
print(f"Threshold for suspicious activity: {FRAUD_THRESHOLD:.6f}")
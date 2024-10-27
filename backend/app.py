from flask import Flask, request, jsonify
import pandas as pd
import torch
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from flask_cors import CORS
import logging
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

logging.basicConfig(level=logging.INFO)

# Load model and tokenizer
model_path = 'llama_fraud_detection_model'
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def prepare_data_for_llama(X):
    return X.apply(lambda row: f"Transaction: {' '.join(map(str, row))}", axis=1).tolist()

@app.route('/predict', methods=['POST'])
def predict():
    app.logger.info("Received a request to /predict")
    
    if 'file' not in request.files:
        app.logger.error("No file part in the request")
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        app.logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Read the CSV file
        df = pd.read_csv(io.StringIO(file.stream.read().decode("UTF8")))
        
        # Limit to 100 rows
        df = df.head(100)
        
        # Prepare the data for the model
        test_data_prepared = prepare_data_for_llama(df)
        
        # Tokenize the data
        encodings = tokenizer(test_data_prepared, truncation=True, padding=True, max_length=512, return_tensors="pt")
        
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
        
        # Add fraud probabilities to the DataFrame
        df['Fraud_Probability'] = fraud_probabilities
        df['Predicted_Fraud'] = df['Fraud_Probability'] > 0.352  # You can adjust this threshold

        # Select suspicious transactions
        suspicious_transactions = df[df['Predicted_Fraud']]

        # Prepare the statistics
        total_transactions = len(df)
        suspicious_count = len(suspicious_transactions)
        print(suspicious_count)
        
        # Extracting required fields
        extracted_data = [
            {
                "Transaction ID": transaction["Transaction ID"],
                "Name": transaction["Cardholder Name"],
                "Device": transaction["Device Information"],
                "Fraud_Probability": transaction["Fraud_Probability"]
            }
            for transaction in suspicious_transactions.to_dict(orient='records')
        ]
        
        # Prepare the response
        response = {
            "total_transactions": total_transactions,
            "suspicious_transactions_count": suspicious_count,
            "suspicious_transactions": extracted_data
        }

        # Displaying the extracted data (for debugging, you can remove this in production)
        for transaction in extracted_data:
            print(transaction)
        
        return jsonify(response)
    
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
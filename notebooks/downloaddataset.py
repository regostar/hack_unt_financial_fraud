import kagglehub
import os

# Create a data directory if it doesn't exist
data_directory = '/content/data/'
os.makedirs(data_directory, exist_ok=True)

# Specify the datasets you want to download
datasets = [
    "kartik2112/fraud-detection",
    "vbinh002/fraud-ecommerce",
    "ealaxi/banksim1",
    "teamincribo/credit-card-fraud",
]

for dataset in datasets:
    try:

        path = kagglehub.dataset_download(dataset)

        # Move the downloaded files to the data directory
        for filename in os.listdir(path):
            os.rename(os.path.join(path, filename), os.path.join(data_directory, filename))

        # Print the path to the downloaded dataset files
        print(f"Downloaded {dataset} to {data_directory}")

    except Exception as e:
        print(f"An error occurred while downloading {dataset}: {e}")


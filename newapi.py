import kaggle
import pandas as pd
import os
from pymongo import MongoClient
from flask import Flask, request, jsonify
from bson import ObjectId

# Authenticate with Kaggle
try:
    kaggle.api.authenticate()
except Exception as e:
    print(f"Error during Kaggle authentication: {e}")
    raise

# Download the dataset
try:
    kaggle.api.dataset_download_files('sahirmaharajj/supply-chain-greenhouse-gas-emission', path='.', unzip=True)
    print("Dataset downloaded successfully.")
except Exception as e:
    print(f"Error downloading dataset: {e}")
    raise

# Check if the CSV file exists
csv_file = 'SupplyChainGHGEmissionFactors_v1.2_NAICS_CO2e_USD2021.csv'
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"The file {csv_file} does not exist. Check if the dataset was downloaded and unzipped correctly.")

# Connect to MongoDB
try:
    client = MongoClient('localhost', 27017)
    db = client['supplychain']
    collection = db['emissions']
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

# Load dataset
try:
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    print("CSV file loaded successfully.")
except Exception as e:
    print(f"Error loading CSV file: {e}")
    raise

# Insert data into MongoDB
try:
    collection.insert_many(df.to_dict('records'))
    print("Data inserted into MongoDB successfully.")
except Exception as e:
    print(f"Error inserting data into MongoDB: {e}")
    raise

# Flask application
app = Flask(__name__)

@app.route('/emissions', methods=['GET'])
def get_emissions():
    # Retrieve all emissions
    emissions = list(collection.find())
    for emission in emissions:
        emission['_id'] = str(emission['_id'])  # Convert ObjectId to string
    return jsonify(emissions)

@app.route('/emission/<id>', methods=['GET'])
def get_emission(id):
    # Retrieve a specific emission
    try:
        emission = collection.find_one({'_id': ObjectId(id)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    if emission:
        emission['_id'] = str(emission['_id'])
        return jsonify(emission)
    else:
        return jsonify({'error': 'Emission not found'}), 404

@app.route('/emission', methods=['POST'])
def add_emission():
    # Add a new emission
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    collection.insert_one(data)
    return jsonify({'message': 'Emission added successfully!'}), 201

@app.route('/emission/<id>', methods=['PUT'])
def update_emission(id):
    # Update an existing emission
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.matched_count:
        return jsonify({'message': 'Emission updated successfully!'})
    else:
        return jsonify({'error': 'Emission not found'}), 404

@app.route('/emission/<id>', methods=['DELETE'])
def delete_emission(id):
    # Delete an emission
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Emission deleted successfully!'})
    else:
        return jsonify({'error': 'Emission not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

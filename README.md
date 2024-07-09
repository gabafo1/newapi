# Supply Chain Greenhouse Gas Emissions API

This project provides an API to interact with a dataset on supply chain greenhouse gas emissions. The dataset is fetched from Kaggle, stored in a MongoDB database, and made accessible through a Flask-based API.

## Prerequisites

- Python 3.x
- Kaggle API
- MongoDB
- Flask
- pandas
- pymongo

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/supply-chain-emissions-api.git
   cd supply-chain-emissions-api
   ```

2. **Install required Python packages:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Set up Kaggle API:**

   - Create a Kaggle account if you don't have one.
   - Go to your account settings and create an API token.
   - Place the downloaded `kaggle.json` file in the `.kaggle` directory in your home folder (e.g., `~/.kaggle/kaggle.json`).

4. **Set up MongoDB:**

   - Install MongoDB and ensure it is running on `localhost:27017`.

## Running the Application

1. **Download the dataset and insert it into MongoDB:**

   ```sh
   python setup.py
   ```

   `setup.py` will:
   - Authenticate with Kaggle
   - Download and unzip the dataset
   - Load the CSV file into a pandas DataFrame
   - Insert the data into a MongoDB collection

2. **Run the Flask API:**

   ```sh
   python app.py
   ```

   The API will be available at `http://localhost:5000`.

## API Endpoints

- **GET /emissions**: Retrieve all emissions records.

  ```sh
  curl -X GET http://localhost:5000/emissions
  ```

- **GET /emission/<id>**: Retrieve a specific emission record by its ID.

  ```sh
  curl -X GET http://localhost:5000/emission/<id>
  ```

- **POST /emission**: Add a new emission record.

  ```sh
  curl -X POST -H "Content-Type: application/json" -d '{"field1":"value1", "field2":"value2"}' http://localhost:5000/emission
  ```

- **PUT /emission/<id>**: Update an existing emission record by its ID.

  ```sh
  curl -X PUT -H "Content-Type: application/json" -d '{"field1":"new_value1"}' http://localhost:5000/emission/<id>
  ```

- **DELETE /emission/<id>**: Delete an emission record by its ID.

  ```sh
  curl -X DELETE http://localhost:5000/emission/<id>
  ```

## License

This project is licensed under the MIT License.
```

### Notes:
- Replace `yourusername` with your actual GitHub username if you intend to upload this project to GitHub.
- Ensure the `requirements.txt` file includes all necessary Python packages. Here's a basic `requirements.txt` content:

```txt
kaggle
pandas
pymongo
flask
```


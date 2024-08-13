from flask import Flask, jsonify, request
from collections import defaultdict


app = Flask(__name__)

Processed_data_store = defaultdict(dict)

# API endpoint for data retrieval
@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    # simulating data fetching
    data = {
        "name":{1: "one",2: "two",3: "three",4: "four",5: "five",6: "six",7: "seven",8: "eight",9: "nine"},
        "money_spend":{1: 10,1: 20,5: 30,6: 40,7: 50,8: 60,9: 70,2: 80,3: 90}
    }

    return jsonify(data)


def process_data(data):
    # converting text to  uppercase ans summing up the numbers
    process_data = {
        
    }


# data storage
@app.route('/process-data', methods=['POST'])
def process_and_store_data():
    # fetching the data 
    data = request.json
    processed_data = process_data(data)


    # simulate storage in memory
    Processed_data_store["data"] = processed_data 
    return jsonify({"message": "data processed and stored successfully"})


# API endpoint forprocessed data retrieval
@app.route('/get-processed-data', methods=['GET'])
def get_processed_data():
    return jsonify(Processed_data_store.get('data', {}))


@app.route('/')
def main():
    return"""
    <h1>Data Processing</h1>
    <p>Endpoints</p>
    <ul>
        <li><a href="/fetch-data">(GET) - Fetch Data</a>
        <li><a href="/process-data">(POST) - Process and Store Data</a>
        <li><a href="/get-processed-data">(GET) - Retrieve Data</a>
    """


if __name__ == '__main__':
    app.run(debug=True)
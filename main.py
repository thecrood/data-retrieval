from flask import Flask, jsonify, request
from collections import defaultdict
import requests

app = Flask(__name__)

Processed_data_store = defaultdict(dict)

# API endpoint for data retrieval
@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    # simulating data fetching
    data = {
        "name":{1: "one",2: "two",3: "three",4: "four",5: "five",6: "six",7: "seven",8: "eight",9: "nine"},
        "money_spend":{1: [10,20],5: 30,6: 40,7: 50,8: 60,9: 70,2: 80,3: 90}
    }

    return jsonify(data),200


def process_data(data):
    # converting text to  uppercase ans summing up the numbers
    processed_data = {}
    for key, value in data["money_spend"].items():
        name = (data["name"][key]).upper()
        # Sum the values if it's a list, otherwise just take the single value
        if isinstance(value, list):
            processed_data[name] = sum(value)
        else:
            processed_data[name] = value
    return processed_data

# data storage
@app.route('/process-data', methods=['POST'])
def process_and_store_data():
    # Make a request to fetch the data from the '/fetch-data' endpoint
    response = requests.get("http://127.0.0.1:5000/fetch-data")
    if response.status_code == 200:
        data = response.json()
    else:
        return jsonify({"error": "Failed to fetch data"}), 500
    processed_data = process_data(data)

    # simulate storage in memory
    Processed_data_store["data"] = processed_data 
    return jsonify({"message": "data processed and stored successfully"}),200


# API endpoint forprocessed data retrieval
@app.route('/get-processed-data', methods=['GET'])
def get_processed_data():
    # get the name from query parameters
    name = request.args.get('name', '').upper()

    data = Processed_data_store['data']
    if name in data:
        return jsonify({name: data[name]}), 200
    else:
        return jsonify({"message": f"Data for {name} not found"}), 404


@app.route('/')
def main():
    return """
    <h1>Data Processing</h1>
    <p>Endpoints</p>
    <ul>
        <li><button onclick="fetchData()">Fetch Data (GET)</button></li>
        <li><button onclick="processData()">Process and Store Data (POST)</button></li>
        <li>
            <form id="dataForm" onsubmit="return fetchProcessedData()">
                <label for="name">Enter Name:</label>
                <input type="text" id="name" name="name" required>
                <button type="submit">Retrieve Data</button>
            </form>
        </li>
    </ul>

    <p id="result"></p>

    <script>
        function fetchData() {
            fetch('/fetch-data', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                alert("Fetched data: " + JSON.stringify(data));
            })
            .catch(error => console.error('Error:', error));
        }

        function processData() {
            // Example data to send in POST request
            const data = {
                key: "value",
                another_key: "another_value"
            };
            
            fetch('/process-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error('Error:', error));
        }

        function fetchProcessedData() {
            const name = document.getElementById('name').value.trim();
            
            fetch(`/get-processed-data?name=${encodeURIComponent(name)}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                const resultElement = document.getElementById('result');
                if (data.message) {
                    resultElement.textContent = data.message;
                } else {
                    // Format the successful response message
                    const name = Object.keys(data)[0];
                    const amount = data[name];
                    resultElement.textContent = `Money spent by ${name} is ${amount}$`;
                }
            })
            .catch(error => console.error('Error:', error));

            // Prevent form submission and page reload
            return false;
        }
    </script>
    """


if __name__ == '__main__':
    app.run(debug=True)
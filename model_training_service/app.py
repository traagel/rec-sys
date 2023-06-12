import subprocess

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()  # Get the JSON payload from the request
    customername = data.get('customername')  # Extract the customername from the payload

    if not customername:
        return jsonify({"error": "No customername provided"}), 400  # If no customername, return an error

    # Run recommend.py script using the subprocess module
    result = subprocess.run(['python', 'recommend.py', '--customer', customername], stdout=subprocess.PIPE)

    # Get the output of recommend.py script
    output = result.stdout.decode()

    # strip output of newlines
    output = output.strip()
    
    # Return the output as a response
    return jsonify({"recommendation": output})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

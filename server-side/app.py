from flask import Flask, request, jsonify
from predictor import predict_esg_score, required_features

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for predicting the ESG score."""
    try:
        # Get the input data from the POST request
        data = request.get_json()

        # Validate if all required fields are present
        if not all(feature in data for feature in required_features):
            return jsonify({'error': 'Missing required features in input data'}), 400

        # Extract the values from the incoming JSON
        user_input = [data[feature] for feature in required_features]

        # Predict ESG score using the input
        esg_score = predict_esg_score(user_input)

        # Return the result as a JSON response
        return jsonify({'esg_score': esg_score})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

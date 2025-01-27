from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# List of required input features for prediction
required_features = [
    'controv_src_score',
    'environmental_pillar_score',
    'governance_pillar_score',
    'social_pillar_score',
    'climate_change_theme_score',
    'industry_adjusted_score',
    'business_ethics_theme_score'
]

# Load the saved model
with open(r"server-side\random_forest_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_esg_score(user_input):
    # Convert user input into a 2D array for the model
    input_array = np.array(user_input).reshape(1, -1)

    # Make a prediction
    prediction = model.predict(input_array)
    ESG_Score = prediction[0]
    return ESG_Score

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the POST request
    data = request.get_json()

    # Extract the values from the incoming JSON
    user_input = [
        data['controv_src_score'],
        data['environmental_pillar_score'],
        data['governance_pillar_score'],
        data['social_pillar_score'],
        data['climate_change_theme_score'],
        data['industry_adjusted_score'],
        data['business_ethics_theme_score']
    ]
    
    # Predict ESG score using the input
    esg_score = predict_esg_score(user_input)

    # Return the result as a JSON response
    return jsonify({'esg_score': esg_score})

if __name__ == "__main__":
    app.run(debug=True)

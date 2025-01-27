import pickle
import numpy as np


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
with open("random_forest_model.pkl", "rb") as f:
    model = pickle.load(f)


def predict_esg_score(user_input):
    print("Started Prediction")
    # user_input = [1.1,1.1,1.1,1,1,1,1]

    # Convert user input into a 2D array for the model
    input_array = np.array(user_input).reshape(1, -1)

    # Make a prediction
    prediction = model.predict(input_array)
    ESG_Score = prediction[0]

    print("\nPredicted ESG Score:", ESG_Score)

    return ESG_Score

if __name__ == "__main__":
    predict_esg_score(1,1,1,1,1,1,1)

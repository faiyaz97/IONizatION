import pickle
import pandas as pd
import numpy as np
import os
 
# List of required input features for prediction
required_features = [
    'controv_src_score',
    'environmental_pillar_score',
    'governance_pillar_score',
    'social_pillar_score',
    'climate_change_theme_score',
    'industry_adjusted_score',
    'business_ethics_theme_score',
    'iva_industry',
    'gics_sub_ind'
]
 
 
def predict(input_data, pickle_path='server-side/random_forest_model.pkl'):
    # Resolve the correct path using os.path
    pickle_path = os.path.join(os.getcwd(), pickle_path.replace('/', os.sep).replace('\\', os.sep))

    # Ensure the file exists
    if not os.path.exists(pickle_path):
        raise FileNotFoundError(f"Model file not found at path: {pickle_path}")

    with open(pickle_path, 'rb') as f:
        objects = pickle.load(f)

    model = objects['model']
    scaler = objects['scaler']
    label_encoders = objects['label_encoders']
    target_encoder = objects['target_encoder']
    features = objects['features']

    input_df = pd.DataFrame([input_data], columns=features)

    # Encode categorical features
    for col in label_encoders:
        input_df[col] = label_encoders[col].transform(input_df[col])

    # Standardize numerical features
    input_scaled = scaler.transform(input_df)

    # Get prediction
    pred = model.predict(input_scaled)
    pred_label = target_encoder.inverse_transform(pred)[0]
    return pred_label
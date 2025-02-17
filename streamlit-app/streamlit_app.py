import streamlit as st
import requests
import pandas as pd

# Flask backend URL (adjust if needed)
FLASK_API_URL = 'http://localhost:5000/predict'

# Load dropdown data
file_path = 'outputFile.csv'
data = pd.read_csv(file_path)

# Extract unique dropdown options
iva_industries = data['iva_industry'].dropna().unique().tolist()
gics_sub_inds = data['gics_sub_ind'].dropna().unique().tolist()

# Full-Screen Layout with 2 columns (Left side with inputs, Right side empty)
col1, col2 = st.columns([1, 1])  # Left side (1), Right side (0, empty)

# Custom CSS to remove margin, padding, and ensure full-screen
st.markdown(
    """
    <style>
        /* Remove default margin and padding from the entire body */
        body {
            margin: 0;
            padding: 0;
            width: 100%;
        }

        /* Remove padding and margin in the reportview-container (Streamlit container) */
        .reportview-container {
            padding: 0 !important;
            margin: 0 !important;
            width: 100%;
        }

        /* Remove padding and margin in the block-container (where the content is inside) */
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            width: 100%;
            max-width: 100%;
        }

        /* Remove default header padding */
        .css-1d391kg .stHeader {
            padding: 0 !important;
        }

        /* Adjust the columns to take full width */
        .stColumn {
            width: 100% !important;
        }

        /* Style the input fields to be smaller */
        .stTextInput, .stNumberInput, .stSelectbox, .stTextArea {
            width: 100% !important;
            max-width: 250px !important;  /* Limiting the width of input fields */
        }

        /* Style the button to take the remaining space */
        .stButton > button {
            width: 100% !important;  /* Make button take up the full width */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the app
col1.header("ESG Score Prediction")

# Left column for input fields and button
with col1:
    # Dynamic number of columns per row (responsive)
    num_columns = 3

    # Create dynamic columns based on num_columns
    cols = st.columns(num_columns)

    # Arrange the input fields in rows
    controv_src_score = cols[0].number_input('Controversy Source', min_value=0.0, max_value=100.0, step=0.1)
    environmental_pillar_score = cols[1].number_input('Environmental Pillar', min_value=0.0, max_value=100.0, step=0.1)
    governance_pillar_score = cols[2].number_input('Governance Pillar', min_value=0.0, max_value=100.0, step=0.1)

    # Move to the next row
    cols = st.columns(num_columns)

    social_pillar_score = cols[0].number_input('Social Pillar', min_value=0.0, max_value=100.0, step=0.1)
    climate_change_theme_score = cols[1].number_input('Climate Change Theme', min_value=0.0, max_value=100.0, step=0.1)
    industry_adjusted_score = cols[2].number_input('Industry Adjusted', min_value=0.0, max_value=100.0, step=0.1)

    # Move to the next row
    cols = st.columns(num_columns)

    business_ethics_theme_score = cols[0].number_input('Business Ethics Theme', min_value=0.0, max_value=100.0, step=0.1)

    # Add dropdowns for IVA Industry and GICS Sub-Industry
    iva_industry = cols[1].selectbox('IVA Industry', iva_industries)
    gics_sub_ind_score = cols[2].selectbox('GICS Sub-Industry', gics_sub_inds)  # Assuming GICS options match IVA

    # Add a button for prediction
    if st.button('Predict ESG Score'):
        # Prepare the input data
        user_input = {
            'controv_src_score': controv_src_score,
            'environmental_pillar_score': environmental_pillar_score,
            'governance_pillar_score': governance_pillar_score,
            'social_pillar_score': social_pillar_score,
            'climate_change_theme_score': climate_change_theme_score,
            'industry_adjusted_score': industry_adjusted_score,
            'business_ethics_theme_score': business_ethics_theme_score,
            'iva_industry': iva_industry,
            'gics_sub_ind': gics_sub_ind_score
        }

        # Make POST request to the backend
        try:
            response = requests.post(FLASK_API_URL, json=user_input)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                esg_score = data.get('esg_score')

                try:
                    # Convert esg_score to float if it's a string
                    esg_score = esg_score
                    st.write(f"Predicted ESG Score: " + esg_score)
                except ValueError:
                    st.write(f"Unexpected response: ESG Score is not a valid number: {esg_score}")
            else:
                st.write(f"Error: {response.json().get('error')}")
        except Exception as e:
            st.write(f"Error connecting to backend: {str(e)}")

from flask import Flask, request, jsonify
import mysql.connector
from predictor import predict_esg_score, required_features
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# # Configure MySQL connection
db_config = {
    'host': 'localhost',       # Update with your MySQL host
    'user': 'root',   # Update with your MySQL username
    'password': 'Kunmannay@3',  # Update with your MySQL password
    'database': 'ionization'   # Update with your MySQL database name
}

# # Function to connect to the database
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/delete', methods=['POST'])
def delete_row():
    """API endpoint to delete a row from the searchdata table based on search_id provided in JSON input."""
    try:
        # Get the input data from the POST request
        data = request.get_json()

        # Validate if search_id is provided in the JSON
        if 'search_id' not in data:
            return jsonify({'error': 'search_id is required in the input data'}), 400

        search_id = data['search_id']

        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the row exists
        check_query = "SELECT * FROM searchdata WHERE search_id = %s"
        cursor.execute(check_query, (search_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({'error': f'No record found with search_id {search_id}'}), 404

        # Delete the row
        delete_query = "DELETE FROM searchdata WHERE search_id = %s"
        cursor.execute(delete_query, (search_id,))
        connection.commit()

        # Close the connection
        cursor.close()
        connection.close()

        return jsonify({'message': f'Record with search_id {search_id} deleted successfully.'})

    except mysql.connector.Error as db_error:
        return jsonify({'error': f"Database error: {str(db_error)}"}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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

        # Save the input data and prediction result to the database
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Define the table structure
            insert_query = """
            INSERT INTO searchdata (controv_src_score, environmental_pillar_score, governance_pillar_score,
                                    social_pillar_score, climate_change_theme_score, industry_adjusted_score,
                                    business_ethics_theme_score, esg_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Execute the insert query
            cursor.execute(insert_query, user_input + [esg_score])
            connection.commit()

        except mysql.connector.Error as db_error:
            return jsonify({'error': f"Database error: {str(db_error)}"}), 500

        finally:
            cursor.close()
            connection.close()

        # Return the result as a JSON response
        return jsonify({'esg_score': float(esg_score)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_all', methods=['GET'])
def get_all_data():
    """API endpoint to retrieve all records from the searchdata table."""
    try:
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get column names in the result

        # Fetch all data from the table
        select_query = "SELECT * FROM searchdata"
        cursor.execute(select_query)
        results = cursor.fetchall()

        # Close the connection
        cursor.close()
        connection.close()

        # Return the results as JSON
        return jsonify(results)

    except mysql.connector.Error as db_error:
        return jsonify({'error': f"Database error: {str(db_error)}"}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

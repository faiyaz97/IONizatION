from flask import Flask, request, jsonify
import mysql.connector
from predictor import predict, required_features
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure MySQL connection
db_config = {
    'host': 'localhost',       # Update with your MySQL host
    'user': 'root',   # Update with your MySQL username
    'password': 'Kunmannay@3',  # Update with your MySQL password
    'database': 'ionization'   # Update with your MySQL database name
}

<<<<<<< Updated upstream

# # Function to connect to the database
=======
# Function to connect to the database
>>>>>>> Stashed changes
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection


# Get all company details Search
@app.route('/get_by_issuerid', methods=['GET'])
def get_by_issuerid():
    """API endpoint to retrieve all details of a particular record based on issuerid."""
    try:
        # Get the issuerid from query parameters
        issuerid = request.args.get('issuerid')  # Get issuerid from the query string
        
        if not issuerid:
            return jsonify({'error': 'issuerid is required'}), 400

        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch the record based on issuerid
        select_query = "SELECT * FROM tabledata WHERE issuerid = %s"
        cursor.execute(select_query, (issuerid,))
        record = cursor.fetchone()

        # Check if record exists
        if not record:
            return jsonify({'error': f'No record found with issuerid {issuerid}'}), 404

        # Remove the 'issuerid' field from the record if it exists
        # if 'issuerid' in record:
        #     del record['issuerid']

        # Close the connection
        cursor.close()
        connection.close()

        # Ensure the record is JSON serializable
        # You may want to explicitly handle any nested structures here
        try:
            
            return jsonify(record)
        except TypeError as e:
            return jsonify({'error': f"Unable to serialize record: {str(e)}"}), 500

    except mysql.connector.Error as db_error:
        return jsonify({'error': f"Database error: {str(db_error)}"}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Delete particular search History
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


# Working with ML Model to predict ESG Score
@app.route('/predict', methods=['POST'])
def predict_route():
    """API endpoint for predicting the ESG score."""
    try:
        # Get the input data from the POST request
        data = request.get_json()

        # Validate if all required fields are present
        if not all(feature in data for feature in required_features):
            return jsonify({'error': 'Missing required features in input data'}), 400

        # Call the predict function
        try:
            # Extract the required input features in order
            user_input = [data[feature] for feature in required_features]
            esg_score = predict(user_input)  # Call the predict function with the input data
        except Exception as model_error:
            return jsonify({'error': f'Model prediction error: {str(model_error)}'}), 500

        # Save the input data and prediction result to the database
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Execute the insert query
            user_input.append(esg_score)
            # Define the table structure
            insert_query = """
    INSERT INTO searchdata (
        controv_src_score, environmental_pillar_score, governance_pillar_score,
        social_pillar_score, climate_change_theme_score, industry_adjusted_score,
        business_ethics_theme_score, iva_industry, gics_sub_ind, esg_score
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
            cursor.execute(insert_query, user_input)
            connection.commit()
        except mysql.connector.Error as db_error:
            return jsonify({'error': f"Database error: {str(db_error)}"}), 500
        finally:
            cursor.close()
            connection.close()

        # Return the result as a JSON response
        return jsonify({'esg_score': esg_score})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Get the whole search history
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


# Function to clear the `searchdata` table
def clear_searchdata_table():
    """Deletes all rows from the searchdata table."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM searchdata")
        connection.commit()
        cursor.close()
        connection.close()
        print("All rows in the 'searchdata' table have been deleted.")
    except mysql.connector.Error as db_error:
        print(f"Database error while clearing table: {db_error}")
    except Exception as e:
        print(f"Error while clearing table: {e}")


if __name__ == "__main__":
    clear_searchdata_table()
    app.run(debug=True)

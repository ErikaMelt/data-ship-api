import pandas as pd
import config
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from predictor import load_file, predict
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)

model = load_file(config.MODEL_PATH)
API_URL = '/static/swagger.json' 

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    config.SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Survival Prediction API"
    },
)

app.register_blueprint(swaggerui_blueprint)

class Prediction(Resource):
    """
    API endpoint for making survival predictions.

    This class handles the POST request to the '/predict' endpoint.
    It expects a JSON payload containing information about the passenger
    and returns the prediction result and probabilities.

    Parameters:
        - passenger_class (str): Passenger class, should be 'first', 'second', or 'third'.
        - gender (str): Gender of the passenger, should be 'male' or 'female'.
        - embarked_from (str): Port of embarkation, should be 'southampton', 'queenstown', or 'cherbourg'.
        - family_size (int): Number of family members.
        - fare (float): Fare amount.
        - age (int): Age of the passenger.

    Returns:
        - predictions (list of int): List of prediction results (0 or 1) for each input.
        - probabilities (list of float): List of prediction probabilities for each class.

    Raises:
        - 400 Bad Request: If the input data is not in the expected format.
        - 500 Internal Server Error: If an unexpected error occurs during prediction.

    Example:
        POST /predict
        {
            "passenger_class": "first",
            "gender": "female",
            "embarked_from": "cherbourg",
            "family_size": 2,
            "fare": 100.0,
            "age": 35
        }

        Response:
        {
            "predictions": [1],
            "probabilities": [[0.2, 0.8]]
        }
    """
    def validate_input(self, data):
        try:
            required_keys = ["passenger_class", "gender", "embarked_from", "family_size", "fare", "age"]
            for key in required_keys:
                if key not in data:
                    return jsonify({"error": f"Missing required key: {key}"}), 400

            valid_passenger_classes = ["first", "second", "third"]
            valid_genders = ["male", "female"]
            valid_ports = ["southampton", "queenstown", "cherbourg"]

            if not isinstance(data["family_size"], int):
                return {"error": "Invalid data type for 'Family Size'. Expected an integer."}, 400

            if not isinstance(data["passenger_class"], str) or data["passenger_class"].lower() not in valid_passenger_classes:
                return {"error": "Invalid data type for 'passenger_class'. Expected 'first', 'second', or 'third'."}, 400

            if not isinstance(data["gender"], str) or data["gender"].lower() not in valid_genders:
                return {"error": "Invalid data type for 'Gender'. Expected 'male' or 'female'."}, 400

            if not isinstance(data["embarked_from"], str) or data["embarked_from"].lower() not in valid_ports:
                return {"error": "Invalid data type for 'Embarked Port'. Expected 'Southampton', 'Queenstown', or 'Cherbourg'."}, 400

            if not isinstance(data["fare"], (int, float)):
                return {"error": "Invalid data type for 'Fare'. Expected an integer or float."}, 400

            if not isinstance(data["age"], int):
                return {"error": "Invalid data type for 'Age'. Expected an integer."}, 400

            return None

        except Exception as e:
            return {"error": f"An error occurred during input validation: {str(e)}"}, 400

    def post(self):
        try:
            data = request.get_json(force=True)

            validation_error = self.validate_input(data)
            if validation_error:
                return validation_error

            df = pd.DataFrame([data])
            df.columns = df.columns.str.lower()
            df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)

            prediction, probability  = predict(model, df)

            # Convert predictions and probabilities to lists for JSON serialization
            predictions_list = prediction.tolist()
            probabilities_list = probability.tolist()

            return jsonify(predictions=predictions_list, probabilities=probabilities_list)
        except ValueError as ve:
            return {"error": f"ValueError: {str(ve)}"}, 400
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500

    @app.route('/ping', methods=['GET'])
    def ping():
        return jsonify({'message': 'API is alive'})


api.add_resource(Prediction, "/predict")
#app.add_url_rule("/ping", "ping", Prediction().ping, methods=['GET'])


if __name__ == "__main__":
    app.run(debug=True)

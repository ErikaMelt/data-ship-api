import pandas as pd
import config
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from predictor import load_file, predict
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)

model = load_file(config.MODEL_PATH)

swaggerui_blueprint = get_swaggerui_blueprint(
    config.SWAGGER_URL,  
    config.API_URL,
    config={  
        'app_name': "Survival Prediction API"
    },
)

app.register_blueprint(swaggerui_blueprint)

class Prediction(Resource):
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

if __name__ == "__main__":
    app.run(debug=True)

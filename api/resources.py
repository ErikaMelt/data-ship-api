import pandas as pd
import config
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from predictor import load_file, predict, validate_input

app = Flask(__name__)
api = Api(app)

model = load_file(config.MODEL_PATH)

class PredictionResource(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)

            validation_error = validate_input(data)
            if validation_error:
                return validation_error

            df = pd.DataFrame([data])
            df.columns = df.columns.str.lower()
            df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)

            prediction, probability = predict(model, df)

            # Convert predictions and probabilities to lists for JSON serialization
            predictions_list = prediction.tolist()
            probabilities_list = probability.tolist()

            return jsonify(predictions=predictions_list, probabilities=probabilities_list)
        except ValueError as ve:
            return {"error": f"ValueError: {str(ve)}"}, 400
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500


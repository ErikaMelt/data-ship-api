from flask_cors import CORS

import config
from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from resources import PredictionResource
from healt_check import PingResource

app = Flask(__name__)
api = Api(app)
CORS(app, origins="*")

swaggerui_blueprint = get_swaggerui_blueprint(
    config.SWAGGER_URL,  
    config.API_URL,
    config={  
        'app_name': "Survival Prediction API"
    },
)

app.register_blueprint(swaggerui_blueprint)
api.add_resource(PredictionResource, "/predict")
api.add_resource(PingResource, "/ping")

if __name__ == "__main__":
    app.run(debug=True)

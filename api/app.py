import config
from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from resources import PredictionResource

app = Flask(__name__)
api = Api(app)

swaggerui_blueprint = get_swaggerui_blueprint(
    config.SWAGGER_URL,  
    config.API_URL,
    config={  
        'app_name': "Survival Prediction API"
    },
)

app.register_blueprint(swaggerui_blueprint)
api.add_resource(PredictionResource, "/predict")

if __name__ == "__main__":
    app.run(debug=True)

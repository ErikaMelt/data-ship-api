from flask_restful import Resource

class PingResource(Resource):
    def get(self):
        try:
            api_status = "successful"
            return {'status': api_status}, 200
        except Exception as e:
            error_message = str(e)
            return {'error': error_message}, 500

from flask import Response, json


class ServerException(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

    def to_response(self):
        data = {'error_message': str(self)}

        return Response(json.dumps(data), status=self.status_code, mimetype='application/json')

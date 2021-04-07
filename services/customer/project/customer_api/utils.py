from flask import Response

def make_response(status_code, response_string):
    my_response = Response(
                response=response_string,
                status=status_code,
                mimetype='application/json'
            )
    return my_response
from rest_framework.response import Response
import dotsi
def serverResponse(response=False, status='', message='', data={}, code=1):
    obj = {
        "response":response,
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    return Response(obj)

def localResponse(response=False,status='', message='', data={}, code=1):
    obj = {
        "response":response,
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    model = dotsi.Dict(obj)
    return model
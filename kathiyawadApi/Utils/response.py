from rest_framework.response import Response
import dotsi
def serverResponse(status='', message='', data={}, code=1):
    obj = {
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    return Response(obj)

def localResponse(status='', message='', data={}, code=1):
    obj = {
        'status': status,
        'code': code,
        'message': message,
        'data': data,
    }
    model = dotsi.Dict(obj)
    return model
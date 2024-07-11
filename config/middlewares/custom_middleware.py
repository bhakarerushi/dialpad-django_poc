
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

class SimpleMiddlware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Preparation ops

        print("MIDDLEWARE EXECUATED ......")


        # if request.method in ['PUT', 'PATCH', 'POST']:
        #     if not request.user.is_superuser:
        #         response = Response("User has no permisssions", status=status.HTTP_403_FORBIDDEN)
        #         response.accepted_renderer = JSONRenderer()
        #         response.accepted_media_type = "application/json"
        #         response.renderer_context = {}
        #         response.render()
        #         return response
        # elif request.method in ['GET']:
        #     if not request.user.is_authenticated:
        #         response = Response("User has no permisssions", status=status.HTTP_403_FORBIDDEN)
        #         response.accepted_renderer = JSONRenderer()
        #         response.accepted_media_type = "application/json"
        #         response.renderer_context = {}
        #         response.render()
        #         return response


        # Retrieving the response
        response = self.get_response(request)

        # Updating the response

        # Returning the response
        return response
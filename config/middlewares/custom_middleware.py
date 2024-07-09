


class SimpleMiddlware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Preparation ops

        print("MIDDLEWARE EXECUATED ......")
        # Retrieving the response
        response = self.get_response(request)

        # Updating the response

        # Returning the response
        return response
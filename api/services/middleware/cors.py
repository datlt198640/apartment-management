from django.utils import translation


class Cors:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        translation.activate("vi_VN")

        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        return response

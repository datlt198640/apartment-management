from rest_framework.views import APIView
from services.helpers.res_utils import ResUtils


class ContactUsView(APIView):

    def get(self, request, format=None):
        data = {
            "Hotline": "(+84) 28 3636 2211 . 3744 2211",
            "Address": "No.10, Street 58, Thao Dien Ward Thu Duc, Ho Chi Minh City, Vietnam",
            "Emaill": "welcome@rosevillasaigon.com",
        }
        return ResUtils.res(data)


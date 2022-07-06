from rest_framework.views import APIView
import random
from services.helpers.res_utils import ResUtils


class ExploreView(APIView):

    def get(self, request, format=None):
        explores = [
            {
                "title": "Stay",
                "description": " Mauris euismod",
                "type": 1,
                "image": "/public/static_image/Stay.png",
                "sub_image": "/public/static_image/sub_static/stay.png",
            },
            {
                "title": "Celebrate",
                "description": " Non commodo",
                "type": 2,
                "image": "/public/static_image/Celebrate.png",
                "sub_image": "/public/static_image/sub_static/celebrate.png",
            },
            {
                "title": "Entertain",
                "description": " Quisque faucibus",
                "type": 3,
                "image": "/public/static_image/Entertain.png",
                "sub_image": "/public/static_image/sub_static/entertain.png",
            },
            {
                "title": "Dine",
                "description": " Curabitur facilisis",
                "type": 4,
                "image": "/public/static_image/Dine.png",
                "sub_image": "/public/static_image/sub_static/dine.png",
            },
            {
                "title": "Shop",
                "description": " Praesent ina",
                "type": 5,
                "image": "/public/static_image/Shop.png",
                "sub_image": "/public/static_image/sub_static/shop.png",
            },
            {
                "title": "Relax",
                "description": " Curabitur metus",
                "type": 6,
                "image": "/public/static_image/Relax.png",
                "sub_image": "/public/static_image/sub_static/relax.png",
            },
        ]

        return ResUtils.res(explores)

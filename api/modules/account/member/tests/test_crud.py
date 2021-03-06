import json
from rest_framework.test import APIClient
from django.test import TestCase
from services.helpers.token_utils import TokenUtils
from ..models import Member
from ..helpers.model_utils import MemberModelUtils
from modules.account.staff.helpers.model_utils import StaffModelUtils

# Create your tests here.


class MemberTestCase(TestCase):
    def setUp(self):
        self.base_url = "/api/v1/account/member/"
        self.base_url_params = "/api/v1/account/member/{}"
        self.model_utils = MemberModelUtils()
        self.staff_model_utils = StaffModelUtils()

        staff = self.staff_model_utils.seeding(1, True)
        staff.user.is_staff = True
        staff.user.save()

        token = TokenUtils.generate_test_token(staff)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

        self.items = self.model_utils.seeding(3)

    def test_list(self):
        resp = self.client.get(self.base_url)
        self.assertEqual(resp.status_code, 200)
        resp = resp.json()
        self.assertEqual(resp["count"], 3)

    def test_detail(self):
        # Item not exist
        resp = self.client.get(self.base_url_params.format(0))
        self.assertEqual(resp.status_code, 404)

        # Item exist
        resp = self.client.get(self.base_url_params.format(self.items[0].pk))
        self.assertEqual(resp.status_code, 200)

    def test_create(self):
        item3 = self.model_utils.seeding(5, True)
        item4 = self.model_utils.seeding(6, True)

        # Add duplicate
        resp = self.client.post(
            self.base_url, json.dumps(item3), content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

        # Add success
        resp = self.client.post(
            self.base_url, json.dumps(item4), content_type="application/json"
        )

        # self.assertEqual(resp.status_code, 200)
        resp = resp.json()
        self.assertEqual(Member.objects.count(), 4)

    def test_edit(self):
        item2 = self.model_utils.seeding(2, True, False)
        # Update not exist
        resp = self.client.put(
            self.base_url_params.format(0),
            json.dumps(item2),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 404)

        # Update duplicate
        resp = self.client.put(
            self.base_url_params.format(self.items[0].pk),
            json.dumps(item2),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_delete(self):
        # Remove not exist
        resp = self.client.delete(self.base_url_params.format(0))
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(Member.objects.count(), 3)

        # Remove single success
        resp = self.client.delete(self.base_url_params.format(self.items[1].pk))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Member.objects.count(), 2)

        # Remove list success
        resp = self.client.delete(
            self.base_url
            + "?ids={}".format(",".join([str(self.items[0].pk), str(self.items[2].pk)]))
        )
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Member.objects.count(), 0)

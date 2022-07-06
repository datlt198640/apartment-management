# import json
# from rest_framework.test import APIClient
# from django.test import TestCase
# from django.contrib.auth.models import Group as Role, Permission
# from services.helpers.token_utils import TokenUtils
# from modules.account.staff.helpers.model_utils import StaffModelUtils
# from ..helpers.model_utils import RoleModelUtils

# # Create your tests here.


# class RoleTestCase(TestCase):
#     def setUp(self):
#         self.base_url = "/api/v1/account/role/"
#         self.base_url_params = "/api/v1/account/role/{}"
#         self.model_utils = RoleModelUtils()
#         staff_model_utils = StaffModelUtils()
#         staff = staff_model_utils.seeding(1, True)
#         staff.user.is_staff = True
#         staff.user.save()

#         token = TokenUtils.generate_test_token(staff)

#         self.client = APIClient()
#         self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

#         self.items = self.model_utils.seeding(3)

#     def test_list(self):
#         response = self.client.get(self.base_url)
#         self.assertEqual(response.status_code, 200)
#         response = response.json()
#         self.assertEqual(response["count"], 3)

#     def test_detail(self):
#         # Item not exist
#         response = self.client.get(self.base_url_params.format(0))
#         self.assertEqual(response.status_code, 404)

#         # Item exist
#         response = self.client.get(self.base_url_params.format(self.items[0].pk))
#         self.assertEqual(response.status_code, 200)

#     def test_create(self):
#         item3 = self.model_utils.seeding(3, True, False)
#         item4 = self.model_utils.seeding(4, True, False)

#         # Add duplicate
#         response = self.client.post(
#             self.base_url, json.dumps(item3), content_type="application/json"
#         )
#         self.assertEqual(response.status_code, 400)

#         # Add success
#         response = self.client.post(
#             self.base_url, json.dumps(item4), content_type="application/json"
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Role.objects.count(), 4)

#     def test_edit(self):
#         item3 = self.model_utils.seeding(3, True, False)

#         # Update not exist
#         response = self.client.put(
#             self.base_url_params.format(0),
#             json.dumps(item3),
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, 404)

#         # Update duplicate
#         response = self.client.put(
#             self.base_url_params.format(self.items[0].pk),
#             json.dumps(item3),
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, 400)

#         # Update success
#         response = self.client.put(
#             self.base_url_params.format(self.items[2].pk),
#             json.dumps(item3),
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, 200)

#     def test_update_permissions(self):
#         # Update 1
#         all_permissions = Permission.objects.all()
#         permissions = [all_permissions[0].pk, all_permissions[1].pk]
#         data = {"permissions": permissions}
#         resp = self.client.put(
#             self.base_url_params.format(self.items[0].pk),
#             json.dumps(data),
#             content_type="application/json",
#         )
#         self.assertEqual(resp.status_code, 200)
#         resp = resp.json()
#         self.assertEqual(resp["permissions"], permissions)

#         # Update 2
#         all_permissions = Permission.objects.all()
#         permissions = [
#             all_permissions[0].pk,
#             all_permissions[3].pk,
#             all_permissions[4].pk,
#         ]
#         data = {"permissions": permissions}
#         resp = self.client.put(
#             self.base_url_params.format(self.items[0].pk),
#             json.dumps(data),
#             content_type="application/json",
#         )
#         self.assertEqual(resp.status_code, 200)
#         resp = resp.json()
#         self.assertEqual(resp["permissions"], permissions)

#     def test_delete(self):
#         # Remove not exist
#         response = self.client.delete(self.base_url_params.format(0))
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(Role.objects.count(), 3)

#         # Remove single success
#         response = self.client.delete(self.base_url_params.format(self.items[0].pk))
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Role.objects.count(), 2)

#         # Remove list success
#         ids = ",".join([str(self.items[1].pk), str(self.items[2].pk)])
#         response = self.client.delete(self.base_url + "?ids={}".format(ids))
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Role.objects.count(), 0)

# import json
# from django.test import TestCase
# from django.utils.translation import gettext as _
# from django.conf import settings
# from rest_framework.test import APIClient
# from services.helpers.utils import Utils
# from services.helpers.token_utils import TokenUtils
# from modules.account.staff.helpers.model_utils import StaffModelUtils


# class AuthTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.model_utils = StaffModelUtils()
#         self.base_url = "/api/v1/auth/"
#         self.staff_base_url = "/api/v1/account/staff/"

#     def test_reset_password(self):
#         staff = self.model_utils.seeding(1, True)
#         data = {
#             "username": str(staff.user.phone_number),
#         }

#         # Step 1 -> request OTP
#         resp = self.client.post(
#             self.base_url + "reset-pwd/",
#             json.dumps(data),
#             content_type="application/json",
#         )

#         status_code = resp.status_code
#         resp = resp.json()
#         verif_id = resp["verif_id"]
#         self.assertEqual(status_code, 200)
#         self.assertTrue("verif_id" in resp)
#         self.assertTrue("username" in resp)

#         # Step 2 -> check OTP
#         otp_payload = {"verif_id": verif_id, "otp_code": settings.DEFAULT_WHITELIST_OTP}
#         resp = self.client.post(
#             "/api/v1/noti/verif/check/",
#             json.dumps(otp_payload),
#             content_type="application/json",
#         )
#         status_code = resp.status_code
#         self.assertEqual(status_code, 200)

#         # Step 3 -> verify
#         password_payload = {"password": "Qwerty!@#4567890"}
#         payload = {**password_payload, **otp_payload}

#         resp = self.client.post(
#             self.base_url + "reset-pwd-verification/",
#             json.dumps(payload),
#             content_type="application/json",
#         )
#         status_code = resp.status_code
#         resp = resp.json()
#         self.assertEqual(status_code, 200)
#         self.assertEqual(resp, {})

#         # Step 4 -> login
#         resp = self.client.post(
#             self.base_url + "login/",
#             json.dumps(
#                 {
#                     "username": str(staff.user.phone_number),
#                     "password": password_payload["password"],
#                 }
#             ),
#             content_type="application/json",
#         )
#         status_code = resp.status_code
#         self.assertEqual(status_code, 200)
#         resp = resp.json()
#         self.assertTrue("token" in resp)

#     def test_change_password(self):
#         staff = self.model_utils.seeding(1, True)
#         token = TokenUtils.generate_test_token(staff)

#         self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

#         data = {
#             "old_password": "Qwerty!@#456",
#             "password": "Qwerty!@#456789",
#         }

#         wrong_data = {
#             "old_password": "password",
#             "password": "Qwerty!@#456789",
#         }

#         # Step 0 -> wrong password
#         resp = self.client.post(
#             self.base_url + "change-pwd/",
#             json.dumps(wrong_data),
#             content_type="application/json",
#         )
#         status_code = resp.status_code
#         self.assertEqual(status_code, 400)
#         resp = resp.json()
#         self.assertEqual(resp["old_password"], _("Incorrect current password"))

#         # Step 1 -> change
#         resp = self.client.post(
#             self.base_url + "change-pwd/",
#             json.dumps(data),
#             content_type="application/json",
#         )
#         status_code = resp.status_code
#         self.assertEqual(status_code, 200)
#         resp = resp.json()
#         self.assertEqual(resp, {})

#         # Step 2 -> login
#         resp = self.client.post(
#             self.base_url + "login/",
#             json.dumps(
#                 {"username": str(staff.user.phone_number), "password": data["password"]}
#             ),
#             content_type="application/json",
#         )
#         status_code = resp.status_code
#         self.assertEqual(status_code, 200)
#         resp = resp.json()
#         self.assertTrue("token" in resp)

#     def test_view_profile(self):
#         staff_data = self.model_utils.seeding(1, True, False)
#         staff = self.model_utils.seeding(1, True)
#         token = TokenUtils.generate_test_token(staff)

#         # Before authenticate
#         resp = self.client.get(
#             self.staff_base_url + "profile/",
#         )
#         self.assertEqual(resp.status_code, 401)

#         self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

#         # After authenticate
#         resp = self.client.get(
#             self.staff_base_url + "profile/",
#         )

#         status_code = resp.status_code
#         self.assertEqual(status_code, 200)
#         resp = resp.json()
#         self.assertEqual(resp["email"], staff_data["email"])

#     def test_update_profile(self):
#         staff = self.model_utils.seeding(1, True)

#         data = {
#             "phone_number": "0906696555",
#             "email": "mail@tbson.info",
#             "fullname": "another name",
#             "gender": 0,
#         }

#         # Before authenticate
#         resp = self.client.put(
#             self.staff_base_url + "profile/",
#             json.dumps(data),
#             content_type="application/json",
#         )
#         self.assertEqual(resp.status_code, 401)

#         token = TokenUtils.generate_test_token(staff)

#         self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

#         # After authenticate
#         resp = self.client.put(
#             self.staff_base_url + "profile/",
#             json.dumps(data),
#             content_type="application/json",
#         )

#         status_code = resp.status_code
#         resp = resp.json()
#         self.assertEqual(status_code, 200)
#         self.assertEqual(
#             resp["phone_number"], Utils.phone_to_canonical_format(data["phone_number"])
#         )
#         self.assertEqual(resp["email"], data["email"])
#         self.assertEqual(resp["fullname"], data["fullname"])
#         self.assertEqual(resp["gender"], data["gender"])

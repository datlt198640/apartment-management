from typing import List, Dict, Any
import re
import os
import sys
import json
import uuid
import asyncio
import hashlib
from functools import wraps
import random
import math
import itertools
import time
from datetime import date, datetime, timedelta
import pytz
import requests
import magic
import phonenumbers
from PIL import Image
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ValidationError
from django.core.cache import caches
from django.http.request import QueryDict
from django.utils.text import slugify
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

MONTH_MAP = {
    1: 1,
    2: 1,
    3: 1,
    4: 2,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 3,
    10: 4,
    11: 4,
    12: 4,
}

QUATER_MAP = {
    1: [1, 2, 3],
    2: [4, 5, 6],
    3: [7, 8, 9],
    4: [10, 1, 12],
}


def async_task(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except Exception:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        if callable(f):
            return loop.run_in_executor(None, f, *args, **kwargs)
        else:
            raise TypeError("Task must be a callable")

    return wrapped


def cache_wrapper(f=None, cache_time=settings.CACHE_TIME):
    cache = caches["default"]

    def cache_return_wrapper_inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cache_key = "{}_{}_{}".format(
                f.__name__,
                str(args[1:] if len(args) and hasattr(args[0], "__dict__") else args),
                str([str(i) for i in kwargs.items()]),
            ).replace(" ", "_")

            cache_key_md5 = hashlib.md5(cache_key.encode("utf-8")).hexdigest()
            cache_key = "cache_return_wrapper" + cache_key_md5
            cache_value = cache.get(cache_key)
            if cache_value is None:
                cache_value = f(*args, **kwargs)
                cache.set(cache_key, cache_value, cache_time)
            return cache_value

        return wrapper

    if f:
        return cache_return_wrapper_inner(f)
    else:
        return cache_return_wrapper_inner


class Utils:
    @staticmethod
    def return_exception(e):
        exc_tb = sys.exc_info()[2]
        file_name = exc_tb.tb_frame.f_code.co_filename
        return str(e) + " => " + file_name + ":" + str(exc_tb.tb_lineno)

    @staticmethod
    def string_to_bool(input: str) -> bool:
        input = input.lower().strip()
        return bool(input and input != "false" and input != "0")

    @staticmethod
    def string_to_int(input: str, default: int = 0) -> int:
        if isinstance(input, str):
            input = input.lower().strip()
        try:
            return int(input)
        except ValueError:
            return default

    @staticmethod
    def string_to_float(input: str, default: float = 0.0) -> float:
        if isinstance(input, str):
            input = input.lower().strip()
        try:
            return float(input)
        except ValueError:
            return default

    @staticmethod
    def get_uuid():
        return uuid.uuid4()

    @staticmethod
    def get_thumbnail(path):
        path_arr = path.split(".")
        path_arr.insert(-1, "thumb")
        return ".".join(path_arr)

    @staticmethod
    def now(aware=False) -> datetime:
        result = datetime.now()
        if not aware:
            return result
        return Utils.make_aware(result)

    @staticmethod
    def now_timestamp() -> int:
        return round(time.time() * 1000)

    @staticmethod
    def today(aware=False) -> date:
        result = date.today()
        if not aware:
            return result
        return Utils.make_aware(result)

    @staticmethod
    def shift_from_now(unit: str, value: int, aware=False):
        params = {unit: value}
        start_date = Utils.now(aware)
        return start_date + timedelta(**params)

    @staticmethod
    def shift_from_today(unit: str, value: int, aware=False):
        params = {unit: value}
        start_date = Utils.today(aware)
        return start_date + timedelta(**params)

    @staticmethod
    def make_aware(input: datetime) -> datetime:
        if not input:
            return input
        tz = pytz.timezone(settings.TIME_ZONE)
        return tz.localize(input)

    @staticmethod
    def scale_image(ratio, path, scale_only=False):
        max_width = settings.IMAGE_MAX_WIDTH
        try:
            image = Image.open(path)
            (original_width, original_height) = image.size
            width = max_width
            if original_width < max_width:
                width = original_width
            height = int(width / ratio) if ratio > 0 else original_height
            width_factor = width / original_width
            height_factor = height / original_height

            factor = width_factor
            if height_factor > width_factor:
                factor = height_factor

            size = (int(original_width * factor), int(original_height * factor))

            if original_width > max_width:
                # Resize to 1 sise fit, 1 side larger than golden rectangle
                image = image.resize(size, Image.ANTIALIAS)
                image.save(path, "JPEG")
                (original_width, original_height) = image.size

            # Crop to golden ratio
            if not scale_only:
                img_x = 0
                img_y = (original_height - height) / 2
                img_width = width
                img_height = height + (original_height - height) / 2
                image = image.crop((img_x, img_y, img_width, img_height))
                image.save(path, "JPEG")
        except Exception:
            pass

    @staticmethod
    def create_thumbnail(width, path):
        try:
            size = (width, width)
            image = Image.open(path)
            image.thumbnail(size, Image.ANTIALIAS)
            image.save(Utils.get_thumbnail(path), "JPEG")
        except Exception:
            pass

    @staticmethod
    def remove_file(path, remove_thumbnail=False):
        if os.path.isfile(path):
            os.remove(path)
            if remove_thumbnail is True:
                thumbnail = Utils.get_thumbnail(path)
                if os.path.isfile(thumbnail):
                    os.remove(thumbnail)

    @staticmethod
    def check_mime(file_buffer):
        mime_type = magic.from_buffer(file_buffer.read(), mime=True)
        mime_source = {
            "image": [
                "image/gif",
                "image/jpeg",
                "image/png",
                "image/psd",
                "image/bmp",
                "image/tiff",
                "image/tiff",
                "image/jp2",
                "image/iff",
                "image/vnd.wap.wbmp",
                "image/xbm",
                "image/vnd.microsoft.icon",
            ],
            "pdf": [
                "application/pdf",
            ],
            "text": [
                "text/plain",
            ],
            "document": [
                "application/msword",
                "application/octet-stream",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "application/vnd.ms-word.document.macroenabled.12",
            ],
            "spreadsheet": [
                "application/excel",
                "application/vnd.ms-excel",
                "application/x-excel",
                "application/x-msexcel",
                "application/vnd.ms-excel.sheet.binary.macroenabled.12",
                "application/vnd.ms-excel.sheet.macroenabled.12",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ],
            "archive": [
                "application/x-rar-compressed",
                "application/x-rar",
                "application/zip",
                "application/x-tar",
                "application/x-7z-compressed",
                "application/gzip",
                "application/tar",
                "application/tar+gzip",
                "application/x-gzip",
            ],
        }
        for filetype, list_mime_type in mime_source.items():
            if mime_type in list_mime_type:
                return filetype
        return ""

    @staticmethod
    def send_email(subject, body, to):
        try:
            if settings.EMAIL_ENABLE is not True or settings.TESTING:
                return
            if not isinstance(to, list):
                to = [str(to)]
            email = EmailMultiAlternatives(
                subject, body, settings.DEFAULT_FROM_EMAIL, to
            )
            email.content_subtype = "html"
            email.attach_alternative(body, "text/html")

            result = email.send()
            return (email, result)
        except Exception as e:
            print(Utils.return_exception(e))
            return e

    @staticmethod
    @async_task
    def send_email_async(*args):
        Utils.send_email(*args)

    @staticmethod
    def user_from_token(token):
        try:
            token = {"token": token}
            data = VerifyJSONWebTokenSerializer().validate(token)
            return data["user"]
        except Exception:
            return None

    @staticmethod
    def user_to_token(user) -> str:
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    @staticmethod
    def lang_from_fontext(context):
        return context["request"].META.get("HTTP_LANG", None)

    @staticmethod
    def lang_from_request(request):
        return request.META.get("HTTP_LANG", None)

    @staticmethod
    def parse_user_related_data(data):
        username = data.pop("username", "")
        if "@" not in username:
            username = Utils.phone_to_canonical_format(username)
        user = {
            "email": data.pop("email", ""),
            "username": username,
            "fullname": data.pop("fullname", ""),
            "password": data.pop("password", ""),
            "groups": data.pop("groups", ""),
        }
        return {"user": user, "remain": data}

    @staticmethod
    def obj_from_pk(model, pk):
        pk = None if not pk else pk
        blank = not pk
        try:
            obj = model.objects.get(pk=pk)
        except model.DoesNotExist:
            obj = None
        return [blank, obj]

    @staticmethod
    def is_testing():
        return len(sys.argv) > 1 and sys.argv[1] == "test"

    @staticmethod
    def is_iso_601_format(date_str: str) -> bool:
        pattern = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}T([0-9]{2}:){2}[0-9]{2}$")
        return bool(pattern.match(date_str))

    @staticmethod
    def format_datetime_str(date_str) -> str:
        if not date_str:
            return None

        meaning_part = date_str

        if "+" in date_str:
            meaning_part = date_str.split("+")[0]

        if "." in meaning_part:
            meaning_part = meaning_part.split(".")[0]

        if Utils.is_iso_601_format(meaning_part):
            return meaning_part
        return None

    @staticmethod
    def datetime_to_str(datetime_obj) -> str:
        if not datetime_obj:
            return None
        date_str = datetime_obj.isoformat()

        if "+" in date_str:
            date_str = date_str.split("+")[0]

        if "." in date_str:
            date_str = date_str.split(".")[0]

        return date_str

    @staticmethod
    def date_to_str(date_obj) -> str:
        if not date_obj:
            return None
        result = Utils.datetime_to_str(date_obj).split("T")[0]
        return result if "." not in result else result.split(".")[0]

    @staticmethod
    def date_to_readble_str(date_obj: date, long_year=True) -> str:
        if not date_obj:
            return None
        if long_year:
            return date_obj.strftime("%d/%m/%Y")
        return date_obj.strftime("%d/%m/%y")

    @staticmethod
    def datetime_to_readble_str(datetime_obj: datetime, long_year=True) -> str:
        if not datetime_obj:
            return None
        if long_year:
            return datetime_obj.strftime("%d/%m/%Y %H:%M:%S")
        return datetime_obj.strftime("%d/%m/%y %H:%M:%S")

    @staticmethod
    def get_str_day(input_date: date) -> str:
        return input_date.strftime("%d")

    @staticmethod
    def get_str_month(input_date: date) -> str:
        month_str = input_date.strftime("%m")
        month_str_map = {
            "01": "A",
            "02": "B",
            "03": "C",
            "04": "D",
            "05": "E",
            "06": "F",
            "07": "G",
            "08": "H",
            "09": "I",
            "10": "J",
            "11": "K",
            "12": "L",
        }
        return month_str_map[month_str]

    @staticmethod
    def get_str_day_month(input_date: date) -> str:
        date_dd = Utils.get_str_day(input_date)
        date_m = Utils.get_str_month(input_date)
        return f"{date_dd}{date_m}"

    @staticmethod
    def readable_str_to_date(date_str):
        if isinstance(date_str, date):
            return date_str
        try:
            format_str = settings.READABLE_DATE_FORMAT
            return datetime.strptime(date_str, format_str)
        except Exception:
            try:
                format_str = settings.STANDARD_DATETIME_FORMAT
                return datetime.strptime(date_str, format_str)
            except Exception:
                return None

    @staticmethod
    def str_to_readable_date_str(date_str: str) -> str:
        try:
            date_obj = Utils.str_to_datetime(date_str)
            return Utils.date_to_readable_str(date_obj)
        except Exception:
            return None

    @staticmethod
    def date_to_readable_str(date_obj, only_date=False) -> str:
        if isinstance(date_obj, datetime):
            if not only_date:
                return date_obj.strftime(settings.READABLE_DATETIME_FORMAT)
            return date_obj.strftime(settings.READABLE_DATE_FORMAT)
        if isinstance(date_obj, date):
            return date_obj.strftime(settings.READABLE_DATE_FORMAT)
        return ""

    @staticmethod
    def str_to_datetime(date_str: str, aware=False):
        format_str = settings.STANDARD_DATETIME_FORMAT
        result = None
        try:
            date_str = Utils.format_datetime_str(date_str)
            result = datetime.strptime(date_str, format_str)
        except Exception:
            pass
        if not aware:
            return result
        return Utils.make_datetime_aware(result)

    @staticmethod
    def str_to_date(date_str: str):
        if not date_str:
            return None

        if "T" in date_str:
            date_str = date_str.split("T")[0]
        if " " in date_str:
            date_str = date_str.split(" ")[0]

        try:
            result = datetime.strptime(date_str, settings.STANDARD_DATE_FORMAT)
            return result.date()
        except Exception:
            return None

    @staticmethod
    def str_to_us_date(date_str: str, field=None):
        if not date_str:
            return None

        if "T" in date_str:
            date_str = date_str.split("T")[0]
        if " " in date_str:
            date_str = date_str.split(" ")[0]

        error_message = None

        try:
            result = datetime.strptime(date_str, settings.US_DATE_FORMAT)
            return result.date()
        except Exception as e:
            error_message = str(e)

        try:
            result = datetime.strptime(date_str, settings.STANDARD_DATE_FORMAT)
            return result.date()
        except Exception as e:
            error_message = str(e)

        if not field:
            raise ValueError(error_message)

        msg = [
            "Invalid date, please use one of the formats:",
            settings.US_DATE_FORMAT,
            "or",
            settings.STANDARD_DATE_FORMAT,
        ]
        raise ValidationError({field: " ".join(msg)})

    @staticmethod
    def get_us_date(input_date, field=None):
        if isinstance(input_date, datetime):
            return input_date.date()
        if isinstance(input_date, date):
            return input_date
        if isinstance(input_date, str):
            return Utils.str_to_us_date(input_date, field)
        return None

    @staticmethod
    def get_next_uid_index(uid: str) -> int:
        return int(re.split("[A-L]", uid)[-1]) + 1 if uid else 1

    @staticmethod
    def clean_key(obj: dict, key: str) -> dict:
        if key in obj:
            obj[key] = Utils.remove_special_chars(str(obj[key]))
        return obj

    @staticmethod
    def clean_and_upper_key(obj: dict, key: str) -> dict:
        if key in obj:
            obj[key] = Utils.remove_special_chars(str(obj[key]), True)
        return obj

    @staticmethod
    def is_semi_contain(_parent: list, _child: list) -> bool:
        parent = set(_parent)
        child = set(_child)
        return not child.isdisjoint(parent) and not child.issubset(parent)

    @staticmethod
    def remove_special_chars(input: str, upper: bool = False) -> str:
        result = slugify(input).replace("-", "").strip()
        if upper:
            return result.upper()
        return result

    @staticmethod
    def str_to_uid(input: str, upper: bool = False) -> str:
        result = slugify(input).replace("-", "_").strip()
        if upper:
            return result.upper()
        return result

    @staticmethod
    def write_file(file: InMemoryUploadedFile, folder: str):
        ext = file.name.split(".")[-1]
        filename = f"{Utils.get_uuid()}.{ext}"
        return default_storage.save(f"{folder}/{filename}", ContentFile(file.read()))
        # return os.path.join(settings.MEDIA_ROOT, path)

    @staticmethod
    def generate_token(user) -> str:
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)

    @staticmethod
    def get_random_number(string_length=6) -> str:
        letters = "0123456789"
        return "".join(random.choice(letters) for i in range(string_length))

    @staticmethod
    def get_random_from_letters(letters: str, length=6) -> str:
        return "".join(random.choice(letters) for i in range(length))

    @staticmethod
    def get_random_password() -> str:
        return "".join(
            [
                Utils.get_random_from_letters("abcdefghijklmnopqrstuvwxyz"),
                Utils.get_random_from_letters("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                Utils.get_random_from_letters("0123456"),
            ]
        )

    @staticmethod
    def get_unusable_password() -> str:
        return "MissVF+JPJoKgMvRQjZTsz9L"

    @staticmethod
    def convert_list_to_string(value):
        if isinstance(value, list) is True:
            return ", ".join(value)
        return value

    @staticmethod
    def convert_string_to_list(str_value):
        if isinstance(str_value, str) is True:
            return [value.strip() for value in str_value.split(",")]
        return []

    @staticmethod
    def phone_to_local_format(phone_number: str) -> str:
        if not phone_number:
            return ""
        prefix = phone_number[0:3]
        if prefix == "+84":
            return "0" + phone_number[3:]
        return phone_number

    @staticmethod
    def phone_to_canonical_format(phone_number: str) -> str:
        if not phone_number:
            return ""
        phone_number = phone_number.replace(" ", "")
        phone_number = phone_number.strip()

        prefix = phone_number[0:4]
        if prefix == "+840":
            return "+84" + phone_number[4:]

        prefix = phone_number[0:1]
        if prefix == "0":
            return "+84" + phone_number[1:]

        return phone_number

    @staticmethod
    def check_valid_phone_number(value):
        if not value:
            return False

        try:
            phone_number = phonenumbers.parse(value, None)
        except phonenumbers.phonenumberutil.NumberParseException:
            try:
                phone_number = phonenumbers.parse(value, "VN")
            except phonenumbers.phonenumberutil.NumberParseException:
                return False
        return bool(phonenumbers.is_valid_number(phone_number))

    @staticmethod
    def get_base_url():
        return f"{settings.PROTOCOL}://{settings.DOMAIN}"

    @staticmethod
    def get_lang_code(request) -> str:
        lang_code = request.META.get("HTTP_ACCEPT_LANGUAGE", settings.LANGUAGE_CODE)
        if lang_code not in ["en-us", "vi-vn"]:
            lang_code = settings.LANGUAGE_CODE
        return lang_code

    @staticmethod
    def password_validate(password):
        """
        password_validate_message = (
            ", ".join(
                [
                    "Passwords must contain at least 8 characters in length",
                    "a minimum of 1 uppercase letter",
                    "a minimum of 1 numeric character",
                ]
            )
        )
        """
        password = password.strip()
        errors = []
        if len(password) < 8:
            errors.append(("Make sure your password is at least 8 letters"))

        if re.search("[0-9]", password) is None:
            errors.append(("Make sure your password has a number in it"))

        if re.search("[A-Z]", password) is None:
            errors.append(("Make sure your password has a capital letter in it"))

        return ". ".join(errors) if errors else ""

    @staticmethod
    def date_str_strip_millisecs(date_input: str) -> str:
        # 2020-02-27T12:15:01.623+07:00
        if not isinstance(date_input, str):
            return None
        if date_input.find(".") == 19 and date_input.find("+") == 23:
            date_arr = date_input.split(".")
            first_part = date_arr[0]
            second_part = date_arr[1][3:]
            return first_part + second_part
        return None

    @staticmethod
    def is_captcha_valid(request):
        captcha_key, source = Utils.get_capthca_headers(request)
        if not all([captcha_key, source]):
            return False

        secret = settings.CAPTCHA_SECRET.get(source)

        response = requests.post(
            settings.CAPTCHA_VALIDATE_URL,
            params={"secret": secret, "response": captcha_key},
        )
        if response.status_code == 200:
            return response.json().get("success")
        return False

    @staticmethod
    def get_capthca_headers(request):
        return (
            request.META.get("HTTP_CAPTCHA_KEY", None),
            request.META.get("HTTP_SOURCE", None),
        )

    @staticmethod
    def check_captcha(request):
        if not settings.CAPTCHA_ENABLED or settings.TESTING:
            return ""

        if not Utils.is_captcha_valid(request):
            return ("Our system detects that you could be a robot. Please try again.")

        return ""

    @staticmethod
    def mask_prefix(input: str, mask_length=4) -> str:
        remain = input[-mask_length:]
        prefix = "*" * (len(input) - mask_length)
        return f"{prefix}{remain}"

    @staticmethod
    def mask_email(email: str) -> str:
        email_arr = email.split("@")
        suffix = email_arr[1]
        name = email_arr[0]
        length = len(name)

        if length == 1:
            return f"*@{suffix}"

        mask_length = math.ceil(length / 2) if length <= 4 else 4
        name = Utils.mask_prefix(name, mask_length)

        return f"{name}@{suffix}"

    @staticmethod
    def mask_username(username):
        if "@" in username:
            return Utils.mask_email(username)
        return Utils.mask_prefix(username)

    @staticmethod
    def get_ip_list(request):
        ips = request.META.get("HTTP_X_FORWARDED_FOR", "")
        return [x.strip() for x in ips.split(",")]

    @staticmethod
    def intersection(lst1, lst2):
        return [value for value in lst1 if value in lst2]

    @staticmethod
    def is_boolean_dict(input: list) -> bool:
        if not input.values():
            return False
        return all(isinstance(item, bool) for item in input.values())

    @staticmethod
    def ensure_space_slash(input: str) -> str:
        return input.replace("/", " / ").replace("  ", " ")

    @staticmethod
    def get_tuple_value(input_tuple, key, default_value=None):
        result_dict = {x: y for x, y in input_tuple}
        return result_dict.get(key, default_value)

    @staticmethod
    def float_equal(float_1: float, float_2: float) -> bool:
        epsilon = sys.float_info.epsilon
        return abs(float_1 - float_2) <= epsilon

    @staticmethod
    def sr_data_to_json(sr_data: Dict) -> Dict:
        return json.loads(JSONRenderer().render(sr_data))

    @staticmethod
    def show_diff_in_secs(time_input) -> float:
        def inner(label: str):
            diff = (Utils.now() - time_input).total_seconds()
            print(f"[+] {label} - {diff} secs")

        return inner

    @staticmethod
    def flat_2d_list(items: List[Any]) -> List[Any]:
        return list(set(itertools.chain.from_iterable(items)))

    @staticmethod
    def get_current_quater() -> int:
        month = Utils.today().month
        return MONTH_MAP.get(month)

    @staticmethod
    def get_quater_from_month(month: int) -> int:
        return MONTH_MAP.get(month)

    @staticmethod
    def get_months_from_quater(quater: int) -> list[int]:
        return QUATER_MAP[quater]

    @staticmethod
    def update_request_payload(payload, new_values: dict) -> QueryDict:
        if isinstance(payload, QueryDict):
            data = payload.copy()
            data.update(new_values)
            return data
        return payload | new_values

    @staticmethod
    def ensure_json(payload, key):
        if key not in payload:
            return
        value = payload.get(key)
        if isinstance(value, str):
            payload.update({key: json.loads(value)})

    @staticmethod
    def get_transfer_data_source(key, title, description=""):
        return dict(
            key=str(key or ""),
            title=str(title or ""),
            description=str(description or ""),
        )

from rest_framework import serializers


class LoginResponseType(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField(max_length=200)
    gender = serializers.IntegerField()
    account_type = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    phone_number = serializers.CharField(max_length=200)
    visible_menus = serializers.ListField(child=serializers.CharField(max_length=200))
    account_type = serializers.CharField(max_length=200)
    token = serializers.CharField(max_length=200)


class ChangePwdRequestType(serializers.Serializer):
    old_password = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)


class ResetPwsRequestType(serializers.Serializer):
    username = serializers.CharField(max_length=200)


class ResetPwsResponseType(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    verif_id = serializers.CharField(max_length=200)


class ResetPwsVerificationRequestType(serializers.Serializer):
    password = serializers.CharField(max_length=200)
    verif_id = serializers.CharField(max_length=200)
    otp_code = serializers.CharField(max_length=200)

from typing import List
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.models import QuerySet
from .utils import Utils


class ModelUtils:
    @staticmethod
    def get(model):
        def inner(*args, **kwargs):
            try:
                if args:
                    pk = args[0]
                    if pk is not None:
                        pk = int(pk)
                    return model.objects.get(pk=pk)
                return model.objects.get(**kwargs)
            except model.DoesNotExist:
                return None

        return inner

    @staticmethod
    def empty_queryset(model):
        return model.objects.filter(pk=None)

    @staticmethod
    def queryset_to_ids(queryset: QuerySet) -> List[int]:
        return [item.pk for item in queryset]

    @staticmethod
    def get_avatar(obj):
        if obj.avatar and hasattr(obj.avatar, "url"):
            if obj.avatar.url.startswith("http"):
                return obj.avatar.url
            return Utils.get_base_url() + obj.avatar.url
        return ""

    @staticmethod
    def create_temp_table_from_queryset(table_name, queryset, using=DEFAULT_DB_ALIAS):
        compiler = queryset.query.get_compiler(using=using)
        sql, params = compiler.as_sql()
        connection = connections[DEFAULT_DB_ALIAS]
        sql = (
            "CREATE TEMP TABLE " + connection.ops.quote_name(table_name) + " AS " + sql
        )
        with connection.cursor() as cursor:

            cursor.execute(
                "DROP TABLE IF EXISTS " + connection.ops.quote_name(table_name)
            )
            cursor.execute(sql, params)
        return table_name

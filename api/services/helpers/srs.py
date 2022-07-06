from rest_framework.serializers import ModelSerializer


class OptionSr(ModelSerializer):
    class Meta:
        model = None
        exclude = []

    def to_representation(self, obj):
        return dict(value=obj.id, label=obj.title)

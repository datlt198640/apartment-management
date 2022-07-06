from django.db.models import Q
from django import forms
from .models import CheckIn
from rest_framework.serializers import ValidationError


class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        exclude = []
    def clean(self):

        super().clean()

        member = self.cleaned_data.get("member")
        check_in_member = CheckIn.objects.filter(
            Q(member=member.id) & Q(check_out=None)
        ).first()
        if check_in_member:
            error_message = (
                "The member does not check out!")
            raise ValidationError(error_message)

        return self.cleaned_data

from django import forms

from .models import CallbackRequest, FeedbackRequest


class CallbackForm(forms.ModelForm):

    class Meta:
        model = CallbackRequest
        fields = [
            'phone',
            'name',
            'comment',
        ]


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = FeedbackRequest
        fields = [
            'name',
            'email',
            'msg_type',
            'msg',
        ]
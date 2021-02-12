from django import forms

from core import const
from sellers.models import Seller
from .models import Group


class SellerSignupForm(forms.ModelForm):

    field_order = [
        'public_name',
        'username',
        'email',
        'password1',
        'password2',
    ]

    class Meta:
        model = Seller
        fields = ['public_name', 'email']
        error_messages = {
            'public_name': {
                'unique': 'Такое название компании уже занято.',
            }
        }

    def signup(self, request, user):
        # Add the user to the sellers group
        sellers_group = Group.objects.get(name=const.SELLERS_GROUPNAME)
        user.groups.add(sellers_group)

        # Create a new Seller database record
        cleaned_data = self.cleaned_data
        Seller.objects.create(
            user=user,
            public_name=cleaned_data['public_name'],
            email=cleaned_data['email'],
        )
        return user
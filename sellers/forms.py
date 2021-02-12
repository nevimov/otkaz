from django import forms

from catalog.models import Window


class WindowForm(forms.ModelForm):
    """
    A form that allows sellers to add a new window or change an existing one.
    """

    def __init__(self, seller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['place'].queryset = seller.places.all()

    class Meta:
        model = Window
        fields = [
            'type',
            'width',
            'height',
            'color',
            'price',
            'description',
            'place',
        ]
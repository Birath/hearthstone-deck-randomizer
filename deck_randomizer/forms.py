from django import forms


class FormatForm(forms.Form):
    OPTIONS = (
        ("wild", "Wild"),
        ("standard", "Standard")
    )
    deck_format = forms.ChoiceField(widget=forms.Select, choices=OPTIONS)


class NameForm(forms.Form):
    name = forms.CharField()


class HeroForm(forms.Form):
    hero = forms.CharField()

from django import forms


class FormatForm(forms.Form):
    OPTIONS = (
        ("a", "Wild"),
        ("b", "Standard")
    )
    deck_format = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)


class NameForm(forms.Form):
    name = forms.CharField()


class HeroForm(forms.Form):
    hero = forms.CharField()

from django import forms


class FormatForm(forms.Form):
    OPTIONS = (
        ("wild", "Wild"),
        ("standard", "Standard")
    )
    deck_format = forms.ChoiceField(widget=forms.Select, choices=OPTIONS,
                                    label="Format")


class NameForm(forms.Form):
    name = forms.CharField(label="Hearthpwn username",
                           initial="CompleteCollection")


class HeroForm(forms.Form):
    OPTIONS = (
        ("random", "Random"),
        ("hunter", "Hunter"),
        ("shaman", "Shaman"),
        ("priest", "Priest"),
        ("mage", "Mage"),
        ("warrior", "Warrior"),
        ("warlock", "Warlock"),
        ("paladin", "Paladin"),
        ("druid", "Druid"),
        ("rogue", "Rogue")
    )
    hero = forms.ChoiceField(widget=forms.Select,
                             choices=OPTIONS,
                             label="Class",
                             )

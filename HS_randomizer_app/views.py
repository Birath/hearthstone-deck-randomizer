from django.shortcuts import render
from deck_randomizer_project.methods import hearthpwn_scarper, get_current_standard_sets, create_dbfid_deck
from HS_randomizer_app.models import Card
from HS_randomizer_app.forms import FormatForm, NameForm, HeroForm
import random
from hearthstone import deckstrings
from hearthstone.enums import FormatType

# Create your views here.
from django.http import HttpResponseRedirect


def index(request):
    hearthpwn_user_name = request.POST.get('user_name', False)
    desired_class = request.POST.get('class', False)
    deck_format = request.POST.get('format', False)
    print(deck_format)
    hero_id = {"priest": 813, "warrior": 7, "rogue": 930, "mage": 1325, "shaman": 1066, "paladin": 671, "hunter": 31,
               "warlock": 893, "druid": 274}

    if request.method != 'POST':
        hero_form = HeroForm()
        name_form = NameForm()
        format_form = FormatForm()
        context = {
            "no_collection": True,
            "name_form": name_form,
            "format_form": format_form,
            "hero_form": hero_form
        }
    else:
        hero_form = HeroForm(request.POST)
        name_form = NameForm(request.POST)
        format_form = FormatForm(request.POST)
        forms = [hero_form, name_form, format_form]
        if all(map(lambda x: x.is_vaild(), forms)):
            return HttpResponseRedirect('/deck/')

    return render(request, "index.html", context)


def generate_deck(request):
    hero_form = HeroForm()
    name_form = NameForm()
    format_form = FormatForm()
    hearthpwn_user_name = name_form.cleaned_data["name"]
    desired_class = hero_form.cleaned_data["hero"]
    deck_format = format_form.cleaned_data["format"]
    owned_cards = hearthpwn_scarper(hearthpwn_user_name, desired_class)
    if deck_format == "standard":
        # TODO implement a way to remove cards non standard card!
        # TODO
        owned_cards = filter(lambda x: )
    random_deck = random.sample(owned_cards, 30)
    standard_sets = get_current_standard_sets()

    deck_format = FormatType.FT_STANDARD
    # Get card image from db by name
    # card[0] -- name of card, card[1] amount of copies owned
    cards = []
    for card in random_deck:
        print("Card name", card[0])
        card_object = Card.objects.get(name__exact=card[0])
        if card_object.set not in standard_sets:
            deck_format = FormatType.FT_WILD
        print([card_object.name, card_object.img_url, card[1]])
        cards.append([card_object.name, card_object.img_url, card[1], card_object.dbfId])

    db_deck = create_dbfid_deck(cards)

    deck = deckstrings.Deck()
    deck.cards = db_deck
    deck.heroes = [hero_id[desired_class.lower()]]
    deck.format = deck_format
    deckstring = deck.as_deckstring
    print(deckstring)
    context = {
        "cards": cards,
        "deckstring": deckstring
    }

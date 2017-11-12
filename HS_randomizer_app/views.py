from django.shortcuts import render
from deck_randomizer_project.methods import hearthpwn_scarper, get_current_standard_sets, create_dbfid_deck
from HS_randomizer_app.models import Card
from HS_randomizer_app.forms import FormatForm, NameForm, HeroForm
import random
from hearthstone import deckstrings
from hearthstone.enums import FormatType
import time


# Create your views here.
from django.http import HttpResponseRedirect


def index(request):
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
        if all(map(lambda x: x.is_valid(), forms)):
            request.session["user_name"] = name_form.cleaned_data['name']
            request.session['hero'] = hero_form.cleaned_data['hero']
            request.session['format'] = format_form.cleaned_data['deck_format']
            return HttpResponseRedirect('/deck/')

    return render(request, "index.html", context)


def generate_deck(request):

    hearthpwn_user_name = request.session.get('user_name')
    desired_class = request.session.get('hero')
    deck_format = request.session.get('format')[0]

    if deck_format == "standard":
        deck_format = FormatType.FT_STANDARD
    else:
        deck_format = FormatType.FT_WILD

    full_collection = hearthpwn_scarper(hearthpwn_user_name, desired_class)
    hero_id = {"priest": 813, "warrior": 7, "rogue": 930, "mage": 637, "shaman": 1066, "paladin": 671, "hunter": 31,
               "warlock": 893, "druid": 274}

    standard_sets = get_current_standard_sets()
    filtered_collection = []
    # Get card image from db by name
    # card[0] -- name of card, card[1] amount of copies owned
    time_before = int(round(time.time() * 1000))
    for card in full_collection:
        card_object = Card.objects.get(name__exact=card[0])
        if deck_format == FormatType.FT_STANDARD and card_object.set not in standard_sets:
            pass
        else:
            if card[1] >= 2:
                filtered_collection.append([card_object.name, card_object.img_url, card[1], card_object.dbfId])
                filtered_collection.append([card_object.name, card_object.img_url, card[1], card_object.dbfId])
            else:
                filtered_collection.append([card_object.name, card_object.img_url, card[1], card_object.dbfId])
    with open("collection.txt", "+w") as f:
        for card in filtered_collection:
            f.write(card[0] + "\n")
    print("DB time", int(round(time.time() * 1000)) - time_before)
    random_deck = random.sample(filtered_collection, 30)
    with open("random_deck.txt", "+w") as f:
        for card in random_deck:
            f.write(card[0] + "\n")
    """
    for card in random_deck:
        print("Card name", card[0])
        card_object = Card.objects.get(name__exact=card[0])
        if card_object.set not in standard_sets:
            deck_format = FormatType.FT_WILD
        print([card_object.name, card_object.img_url, card[1]])
        cards.append([card_object.name, card_object.img_url, card[1], card_object.dbfId])
    """

    db_deck = create_dbfid_deck(random_deck)
    print(db_deck)
    print(len(db_deck))

    print([hero_id[desired_class.lower()]], deck_format)

    deck = deckstrings.Deck()
    deck.cards = db_deck
    deck.heroes = [hero_id[desired_class.lower()]]
    deck.format = deck_format
    deckstring = deck.as_deckstring
    print(deckstring)
    context = {
        "cards": random_deck,
        "deckstring": deckstring
    }
    return render(request, "deck.html", context)




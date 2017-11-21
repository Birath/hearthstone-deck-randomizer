import random
import time

from deck_randomizer.forms import FormatForm, NameForm, HeroForm
from deck_randomizer.models import Card
from deck_randomizer.utils import hearthpwn_scarper, \
    get_current_standard_sets, create_dbfid_deck, get_filtered_collection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from hearthstone import deckstrings
from hearthstone.enums import FormatType


# Create your views here.
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
        return render(request, "index.html", context)
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


def generate_deck(request):

    hearthpwn_user_name = request.session.get('user_name')
    desired_class = request.session.get('hero')
    deck_format = request.session.get('format')[0]

    if deck_format == "standard":
        deck_format = FormatType.FT_STANDARD
    else:
        deck_format = FormatType.FT_WILD

    # Get collection from session if possible, saves time due to no request
    if not request.session.get('full_collection', default=False):
        print("Getting collection from Hearthpwn")
        full_collection = hearthpwn_scarper(hearthpwn_user_name)
        request.session["full_collection"] = full_collection
    else:
        print("Getting collection from session")
        full_collection = request.session.get("full_collection")

    hero_collection = get_filtered_collection(full_collection, desired_class)
    hero_id = {"priest": 813, "warrior": 7, "rogue": 930, "mage": 637,
               "shaman": 1066, "paladin": 671, "hunter": 31,
               "warlock": 893, "druid": 274}
    standard_sets = get_current_standard_sets()

    if not standard_sets:
        standard_sets = ["Basic", "Classic", "Whispers of the Old Gods",
                         "One Night in Karazhan",
                         "Mean Streets of Gadgetzan",
                         "Journey to Un'Goro",
                         "Knights of the Frozen Throne",
                         "Kobolds & Catacombs"]

    filtered_collection = []
    # Get card data from the database by card name
    # card[0] name of card, card[1] amount of copies owned
    time_before = int(round(time.time() * 1000))
    for card in hero_collection:
        print("Card", type(card[0]))
        card_object = Card.objects.get(name__exact=card[0])
        # Only add cards from standard format if standard format is chosen
        if deck_format == FormatType.FT_STANDARD and card_object.set\
                not in standard_sets:
            pass
        else:
            # Add two cards if user owns more than two copies
            if card[1] >= 2:
                filtered_collection += [[card_object.name,
                                        card_object.img_url, card[1],
                                        card_object.dbfId]] * 2
                # filtered_collection.append([card_object.name,
                #                             card_object.img_url,
                #                             card[1], card_object.dbfId])
            else:
                filtered_collection.append([card_object.name,
                                            card_object.img_url,
                                            card[1], card_object.dbfId])
    print("DB time", int(round(time.time() * 1000)) - time_before)

    # Create a deck by picking 30 random cards
    random_deck = random.sample(filtered_collection, 30)
    # Debug
    # with open("random_deck.txt", "+w") as f:
    #     for card in random_deck:
    #         f.write(card[0] + "\n")

    # Creates the deckstring the hearthstone python module
    db_deck = create_dbfid_deck(random_deck)
    deck = deckstrings.Deck()
    deck.cards = db_deck
    deck.heroes = [hero_id[desired_class.lower()]]
    deck.format = deck_format
    deckstring = deck.as_deckstring

    context = {
        "cards": random_deck,
        "deckstring": deckstring
    }
    return render(request, "deck.html", context)

import random

from django.http import JsonResponse
from django.shortcuts import render
from hearthstone import deckstrings
from hearthstone.enums import FormatType

from deck_randomizer.forms import FormatForm, NameForm, HeroForm
from deck_randomizer.models import Card
from deck_randomizer.utils import hearthpwn_scarper, \
    get_current_standard_sets, create_dbfid_deck, get_filtered_collection, \
    get_amount_of_cards


# Create your views here.
def index(request):
    if request.method != 'POST':
        hero_form = HeroForm()
        name_form = NameForm()
        format_form = FormatForm()
        context = {
            "name_form": name_form,
            "format_form": format_form,
            "hero_form": hero_form
        }
        return render(request, "index.html", context)


def generate_deck(request):

    desired_class = request.GET.get('hero')
    deck_format = request.GET.get('format')

    if deck_format == "standard":
        deck_format = FormatType.FT_STANDARD
    else:
        deck_format = FormatType.FT_WILD

    print("Getting collection from session")
    full_collection = request.session.get("full_collection")

    hero_collection = get_filtered_collection(full_collection, desired_class)
    hero_id = {"priest": 813, "warrior": 7, "rogue": 930, "mage": 637,
               "shaman": 1066, "paladin": 671, "hunter": 31,
               "warlock": 893, "druid": 274}
    # False if bad api request, TODO add way to automatically update
    standard_sets = get_current_standard_sets()
    if not standard_sets:
        standard_sets = ["Basic", "Classic", "Whispers of the Old Gods",
                         "One Night in Karazhan",
                         "Mean Streets of Gadgetzan",
                         "Journey to Un'Goro",
                         "Knights of the Frozen Throne",
                         "Kobolds & Catacombs"]

    filtered_collection = []
    for card in hero_collection:
        card_object = Card.objects.get(name__exact=card[0])
        # Only add cards from standard format if standard format is chosen
        if deck_format == FormatType.FT_STANDARD and card_object.set \
                not in standard_sets:
            pass
        else:
            # Add two cards if user owns more than two copies
            if card[1] >= 2:
                filtered_collection += [[card_object.name,
                                         card_object.img_url, card[1],
                                         card_object.dbfId]] * 2
            else:
                filtered_collection.append([card_object.name,
                                            card_object.img_url,
                                            card[1], card_object.dbfId])

    # Create a deck by picking 30 random cards
    random_deck = random.sample(filtered_collection, 30)

    final_deck = []
    for card in random_deck:
        if card == random_deck[0]:
            final_deck.append((card[0], 1))
        elif card in final_deck:
            final_deck[final_deck.index(card)][1] = 2
        else:
            final_deck.append((card[0], 1))

    # Creates the deckstring the hearthstone python module
    db_deck = create_dbfid_deck(random_deck)
    deck = deckstrings.Deck()
    deck.cards = db_deck
    if desired_class == "random":
        deck.heroes = [random.choice(list(hero_id.values()))]
    else:
        deck.heroes = [hero_id[desired_class.lower()]]
    deck.format = deck_format
    deckstring = deck.as_deckstring

    context = {
        "cards": final_deck,
        "deckstring": deckstring
    }

    return render(request, "deck.html", context)


def import_collection(request):
    name = request.GET.get('name')
    full_collection = hearthpwn_scarper(name)
    if full_collection is False:
        answer = "Could not import collection. Make sure that your hearthpwn "\
                 "collection is set to public and try again"

    else:
        request.session["full_collection"] = full_collection
        cards_owned = get_amount_of_cards(full_collection)
        answer = "Imported {} cards from {}'s collection".format(cards_owned,
                                                                 name)
    data = {
        "response": answer
    }
    return JsonResponse(data)


def update_test(request):
    # https://stackoverflow.com/questions/45906858/update-dom-without-reloading-the-page-in-django
    print("I got here")
    name = request.GET.get('name')
    hero = request.GET.get('hero')
    deck_format = request.GET.get('format')
    answer = 'Your hearthpwn name is {} and you choose {} in the {} ' \
             'format'.format(name, hero, deck_format)

    data = {
        'response': answer
    }
    return JsonResponse(data)

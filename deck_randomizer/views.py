import random
import time

from django.http import JsonResponse
from django.shortcuts import render
from hearthstone import deckstrings
from hearthstone.enums import FormatType

from deck_randomizer.forms import FormatForm, NameForm, HeroForm
from deck_randomizer.models import Card
from deck_randomizer.utils import hearthpwn_scarper, \
    get_standard_sets, create_dbfid_deck, get_filtered_collection, \
    get_amount_of_cards


# Create your views here.
def index(request):
    hero_form = HeroForm()
    name_form = NameForm()
    format_form = FormatForm()

    if (request.session.get("full_collection", False) and
            request.session.get("name", False)):
        name = request.session.get("name")
        name_form = NameForm(initial={'name': name})
        cards_owned = get_amount_of_cards(
            request.session.get("full_collection")
        )
        cards_owned_txt = "Imported {} cards ({} unique) from {}'s " \
                          "collection".format(cards_owned[1],
                                              cards_owned[0],
                                              name)
        context = {
            "name_form": name_form,
            "format_form": format_form,
            "hero_form": hero_form,
            "card_amount": cards_owned_txt,
        }
    else:
        context = {
            "name_form": name_form,
            "format_form": format_form,
            "hero_form": hero_form
        }

    return render(request, "index.html", context)


def generate_deck(request):
    hero_id = {"priest": 813, "warrior": 7, "rogue": 930, "mage": 637,
               "shaman": 1066, "paladin": 671, "hunter": 31,
               "warlock": 893, "druid": 274}
    gen_start_time = time.clock()
    desired_class = request.GET.get('hero')
    if desired_class == "random":
        desired_class = random.choice(list(hero_id.keys()))
    deck_format = request.GET.get('format')

    if deck_format == "standard":
        deck_format = FormatType.FT_STANDARD
    else:
        deck_format = FormatType.FT_WILD

    print("Getting collection from session")
    full_collection = request.session.get("full_collection")

    class_collection = get_filtered_collection(full_collection, desired_class)

    standard_sets = get_standard_sets()

    rarity_colors = {
        "Free": "#000",
        "Common": "#000",
        "Rare": "#0070dd",
        "Epic": "#a335ee",
        "Legendary": "#ff8000"
    }


    filtered_collection = []
    for card in class_collection:
        card_object = Card.objects.get(name__exact=card[0])
        # Only add cards from standard format if standard format is chosen
        if (deck_format == FormatType.FT_STANDARD and
                card_object.set not in standard_sets):
            pass
        else:
            # Add two cards if user owns more than two copies
            card_amount = card[1]
            if card_amount >= 2:
                filtered_collection += [
                                        [card_object.name,
                                         card_object.img_url,
                                         card_amount,
                                         card_object.dbfId,
                                         rarity_colors[card_object.rarity],
                                         card_object.cost]
                                        ] * 2
            else:
                filtered_collection.append([card_object.name,
                                            card_object.img_url,
                                            card_amount,
                                            card_object.dbfId,
                                            rarity_colors[card_object.rarity],
                                            card_object.cost])

    # Create a deck by picking 30 random cards
    random_deck = random.sample(filtered_collection, 30)

    final_deck = []
    # Merge duplicates
    for card in random_deck:
        name = card[0]
        rarity = card[4]
        cost = card[5]
        if card == random_deck[0]:
            final_deck.append((name, 1, rarity, cost))
        elif card in final_deck:
            final_deck[final_deck.index(card)][1] = 2
        else:
            final_deck.append((name, 1, rarity, cost))
    # Sort cards by mana cost
    sorted_deck = sorted(final_deck, key=lambda x: x[3])

    # Creates the deckstring using the hearthstone python module
    db_deck = create_dbfid_deck(random_deck)
    deck = deckstrings.Deck()
    deck.cards = db_deck
    deck.heroes = [hero_id[desired_class]]
    deck.format = deck_format
    deckstring = deck.as_deckstring
    gen_end_time = time.clock()
    print("Total gen time", gen_end_time - gen_start_time)
    context = {
        "cards": sorted_deck,
        "class": desired_class.title(),
        "deckstring": deckstring,
    }

    return render(request, "deck.html", context)


def import_collection(request):
    name = request.GET.get('name')
    try:
        full_collection = hearthpwn_scarper(name)
    except ConnectionError:
        answer = "Something went wrong when connecting to Hearthpwn, " \
                 "try again later "
        data = {
            "response": answer
        }
        return JsonResponse(data)
    if full_collection is False:
        answer = "Could not import collection. Make sure that your " \
                 "<a href='http://www.hearthpwn.com/members/{}/collection'>" \
                 "Hearthpwn collection</a> is set to public " \
                 "and try again.".format(name)

    else:
        request.session["full_collection"] = full_collection
        request.session["name"] = name
        cards_owned = get_amount_of_cards(full_collection)
        answer = "Imported {} cards ({} unique) from " \
                 "{}'s collection".format(cards_owned[1], cards_owned[0], name)
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

import json
import sys

import requests
from deck_randomizer.models import Card


def get_cards():
    """
    Gets all current collectible cards from omgvamp's Mashape
    Hearthstone API, and returns them as a json object"
    :return: A JSON object of all current collectible cards
    """
    # NOTE Remove this later
    mashape_key = "29ivbg2fYEmshQaND2mqbZPrtyG6p11uiSQjsnyKBEOkALj6J1"
    url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards?collectible=1"
    headers = {"X-Mashape-Key": mashape_key}
    response = requests.get(url, headers=headers)
    try:
        cards = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print("Failed to decode response, possibly empty")
        print("Response:", response.text)
        sys.exit(-1)
    return cards


def update_card_db(cards):
    """
    Updates the card database
    Usage: run python manage.py shell, import Card model and this file,
    get all current cards from get_cards and then run update_card_db
    :param cards: a json object containing the cards to update
    :return: None
    """
    # First clears the database
    # TODO Move database update into separate function
    print("Populating card database...")
    for cardset, cards in cards.items():
        # Check that current item actually is a collectible card
        if cardset not in ["Hero Skins", "Tavern Brawl", "Missions", "Credits",
                           "System", "Debug"]:
            for card_data in cards:
                # An exception is required for death knights
                if card_data["type"] != "Hero":
                    try:
                        c = Card.objects.get(name__exact=card_data["name"])
                        c.name = card_data["name"]
                        c.hero = card_data["playerClass"]
                        c.img_url = card_data["img"]
                        c.dbfId = card_data["dbfId"]
                        c.set = card_data["cardSet"]
                        c.save()
                    except Card.DoesNotExist:
                        c = Card(name=card_data["name"],
                                 hero=card_data["playerClass"],
                                 img_url=card_data["img"],
                                 dbfId=card_data["dbfId"],
                                 set=card_data["cardSet"])
                    c.save()
                # Death knights are of the type hero and are legendary
                elif (card_data["type"] == "Hero" and
                      card_data["rarity"] == "Legendary"):
                    try:
                        c = Card.objects.get(name__exact=card_data["name"])
                        c.name = card_data["name"]
                        c.hero = card_data["playerClass"]
                        c.img_url = card_data["img"]
                        c.dbfId = card_data["dbfId"]
                        c.set = card_data["cardSet"]
                        c.save()
                    except Card.DoesNotExist:
                        c = Card(name=card_data["name"],
                                 hero=card_data["playerClass"],
                                 img_url=card_data["img"],
                                 dbfId=card_data["dbfId"],
                                 set=card_data["cardSet"])
                        c.save()
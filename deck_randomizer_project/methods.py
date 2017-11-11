import requests
import json
import sys
from bs4 import BeautifulSoup
from HS_randomizer_app.models import Card


def hearthpwn_scarper(user_name, player_class):
    """ Get users collection from hearthpwn and returns it as list
    Parameters:
        user_name -- Hearthpwn user_name
    """
    url = "http://www.hearthpwn.com/members/{}/collection".format(user_name)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    owned_cards = soup.find_all(True, {"data-card-class":[player_class.upper(), "NONE"], 'class': 'owns-card'})
    owned_cards_data = []
    dups = []
    for card in owned_cards:
        card_name = card['data-card-name']
        card_count = card.find(class_='inline-card-count')['data-card-count']
        print(card_name, card_count)
        print(any(map(lambda x: card_name == x[0], owned_cards_data)))
        # Checks for duplicates (Golden cards)
        if not any(map(lambda x: card_name in x[0], owned_cards_data)):
            if card_count == 2:
                owned_cards_data.append((card_name, card_count))
                owned_cards_data.append((card_name, card_count))
            else:
                owned_cards_data.append((card_name, card_count))
        else:
            print("found duplicate")
            dups.append((card_name, card_count))
    for dup in dups:
        print(dup)
        """
        if card['data-card-name'] not in owned_cards_data:
            owned_cards_data.append((card_name, card_count))
        else:
            print("found duplicate")
        """

    return owned_cards_data


def get_cards():
    """ Gets all current collectible cards from omgvamp's mashape
    Hearthstone API, and returns them as a json object"""
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


def create_dbfid_deck(deck):
    seen = []
    res = []
    for card in deck:
        if card not in seen:
            res.append((int(card[3]), 1))
            seen.append(card)
        else:
            card_to_uppdate = res.index(int(card[3]), 1)
            res[card_to_uppdate] = (int(card[3]), 2)
    return res


def get_current_standard_sets():
    """ Gets all current sets in standard mode from omgvamp's mashape
    Hearthstone API and returns them as a json object"""
    url = "https://omgvamp-hearthstone-v1.p.mashape.com/info"
    mashape_key = "29ivbg2fYEmshQaND2mqbZPrtyG6p11uiSQjsnyKBEOkALj6J1"
    headers = {"X-Mashape-Key": mashape_key}
    response = requests.get(url, headers=headers)
    try:
        sets = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print("Failed to decode response, possibly empty")
        print("Response:", response.text)
        sys.exit(-1)
    print(sets["standard"])
    return sets["standard"]


def update_card_db(cards):
    """ Updates the card database
    Usage: run python manage.py shell, import Card model and this file,
    get all current cards from get_cards and then run update_card_db

    Parameters:
        cards -- a json object containing the cards to updated
    """
    # First clears the database
    # Card.objects.all().delete()
    print("Populating card database...")
    for cardset, cards in cards.items():
        # Remove non cards that are marked as collectible
        if cardset not in ["Hero Skins", "Tavern Brawl", "Missions", "Credits", "System", "Debug"]:
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
                        c = Card(name=card_data["name"], hero=card_data["playerClass"], img_url=card_data["img"],
                                 dbfId=card_data["dbfId"], set=card_data["cardSet"])
                    c.save()
                elif card_data["type"] == "Hero" and card_data["rarity"] == "Legendary":
                    try:
                        c = Card.objects.get(name__exact=card_data["name"])
                        c.name = card_data["name"]
                        c.hero = card_data["playerClass"]
                        c.img_url = card_data["img"]
                        c.dbfId = card_data["dbfId"]
                        c.set = card_data["cardSet"]
                        c.save()
                    except Card.DoesNotExist:
                        c = Card(name=card_data["name"], hero=card_data["playerClass"], img_url=card_data["img"],
                                 dbfId=card_data["dbfId"], set=card_data["cardSet"])
                        c.save()


if __name__ == "__main__":
    # hearthpwn_scarper("Fuddu")
    update_card_db(get_cards())

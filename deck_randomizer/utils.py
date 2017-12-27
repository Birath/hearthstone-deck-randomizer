import configparser
import json
import os
import sys

import requests
from bs4 import BeautifulSoup


def hearthpwn_scarper(user_name):
    """ Get users collection from hearthpwn and returns it as list
    of tuples with card name and card count
    Parameters:
        user_name -- Hearthpwn user name
    """
    url = "http://www.hearthpwn.com/members/{}/collection".format(user_name)
    try:
        page = requests.get(url)
    except requests.exceptions.ConnectionError:
        raise ConnectionError
    response = BeautifulSoup(page.content, 'html.parser')
    if response.find(text='Not found') is not None \
            or response.find(text='This user has no collection') is not None \
            or response.find(
            text="This user's collection is private.") is not None:
        return False

    else:
        # Decodes the page as a string to store in session
        # TODO Figure out why this works
        page_content = response.decode('utf-8')
        return page_content


def get_amount_of_cards(collection_content):
    """
    Calculates the amount of cards in a collection
    :param collection_content: A collection decoded in utf-8
    :return: Total amount of cards in a collection
    """
    collection_page = BeautifulSoup(collection_content.encode(), 'html.parser')
    amount_of_cards = len(collection_page.find_all(True,
                                                   {'class': 'owns-card'}))
    return amount_of_cards


def get_filtered_collection(collection_page, player_class):
    """
    Filter out cards from classes other than the chosen one
    :param collection_page: Users collection from hearthpwn as a html page,
    :param player_class: Chosen hero
    :return: A list of all owned cards of the chosen hero + neutrals
    """
    collection_page = collection_page.encode()
    card_collection = BeautifulSoup(collection_page, 'html.parser')
    owned_cards = card_collection.find_all(True, {"data-card-class":
                                                  [player_class.upper(),
                                                   "NONE"],
                                                  'class': 'owns-card'})
    print(len(owned_cards))
    owned_cards_data = []
    for card_data in owned_cards:
        card_name = card_data['data-card-name']
        card_count = int(card_data.find(
            class_='inline-card-count')['data-card-count'])
        owned_cards_data.append((card_name, card_count))

    return owned_cards_data


def create_dbfid_deck(deck):
    """Takes a hearthstone deck and returns a list
     containing dbf id's of all cards and the amount in the deck

    :param deck: a list of a hearthstone deck, where each card is a list
    of information
    :return:
    """
    seen = []
    res = []
    for card_data in deck:
        dbfid = card_data[3]
        if card_data not in seen:
            res.append((int(dbfid), 1))
            seen.append(card_data)
        else:
            card_to_update = res.index((int(dbfid), 1))
            res[card_to_update] = (int(dbfid), 2)
    return res


def get_current_standard_sets():
    """
    Gets all current sets in standard mode from omgvamp's Mashape
    Hearthstone API and returns them as a JSON object
    :return: A JSON object if api request is successful, else false
    """
    url = "https://omgvamp-hearthstone-v1.p.mashape.com/info"
    # Get api key from config file
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.abspath(os.path.dirname(
        os.path.dirname(__file__))),
        "config.ini")
    config.read(config_path)
    mashape_key = config["Mashape"]["mashapekey"]
    headers = {"X-Mashape-Key": mashape_key}
    response = requests.get(url, headers=headers)
    # Raises error if bad response
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("API request for standard sets failed")
        raise ConnectionError
    try:
        sets = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print("Failed to decode response, possibly empty")
        print("Response:", response.text)
        sys.exit(-1)
    return sets["standard"]


def get_standard_sets():
    standard_sets = ["Basic", "Classic", "Whispers of the Old Gods",
                     "One Night in Karazhan",
                     "Mean Streets of Gadgetzan",
                     "Journey to Un'Goro",
                     "Knights of the Frozen Throne",
                     "Kobolds & Catacombs"]
    return standard_sets

import requests
import json
import sys
from bs4 import BeautifulSoup


def hearthpwn_scarper(user_name, player_class):
    """ Get users collection from hearthpwn and returns it as list
    of tuples with card name and card count
    Parameters:
        user_name -- Hearthpwn user_name
    """
    url = "http://www.hearthpwn.com/members/{}/collection".format(user_name)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    owned_cards = soup.find_all(True, {"data-card-class":[player_class.upper(), "NONE"], 'class': 'owns-card'})
    owned_cards_data = []
    # dups = []
    for card_data in owned_cards:
        card_name = card_data['data-card-name']
        card_count = int(card_data.find(class_='inline-card-count')['data-card-count'])
        # print(card_name, card_count)
        # print(any(map(lambda x: card_name == x[0], owned_cards_data)))
        # Checks for Only add
        # if not any(map(lambda x: card_name in x[0], owned_cards_data)):
        # if card_count >= 2:
        #    owned_cards_data.append((card_name, card_count))
        #    owned_cards_data.append((card_name, card_count))
        # else:
        owned_cards_data.append((card_name, card_count))
        # else:
        #   dups.append((card_name, card_count))
    # for dup in dups:
    #    print(dup)
        """
        if card['data-card-name'] not in owned_cards_data:
            owned_cards_data.append((card_name, card_count))
        else:
            print("found duplicate")
        """

    return owned_cards_data


def create_dbfid_deck(deck):
    """Takes a hearthstone deck and returns a list
     containing dbf id's of all cards and the amount in the deck

    :param deck: a list of a hearthstone deck, where each card is a list of information
    :return:
    """
    seen = []
    res = []
    for card_data in deck:
        print(card_data)
        if card_data not in seen:
            res.append((int(card_data[3]), 1))
            seen.append(card_data)
        else:
            print("Contains dups")
            card_to_update = res.index((int(card_data[3]), 1))
            res[card_to_update] = (int(card_data[3]), 2)
    for dbid in res:
        print(dbid, ",")
    for s in seen:
        print(s)
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


if __name__ == "__main__":
    collection = hearthpwn_scarper("Fuddu", "mage")

    with open("collection.txt", "+w") as f:
        for card in collection:
            f.write(card[0] + "\n")
    # update_card_db(get_cards())

    TEST_DECKSTRING_CARDLIST = (
        (38521, 1),  # Alleycat
        (308, 1),  # Jeweled Macaw
        (38408, 1),  # Cat Trick
        (985, 1),  # Crackling Razormaw
        (41524, 1),  # Dinomancy
        (443, 1),  # Freezing Trap
        (43029, 1),  # Kindly Grandmother
        (1686, 1),  # Stubborn Gastropod
        (40496, 1),  # Animal Companion
        (609, 1),  # Eaglehorn Bow
        (40921, 1),  # Eggnapper
        (790, 1),  # Kill Command
        (45307, 1),  # Rat Pack
        (39003, 1),  # Houndmaster
        (768, 1),  # Infested Wolf
        (42782, 1),  # Nesting Roc
        (41257, 1),  # Tundra Rhino
        (281, 1),  # Savannah Highmane
        (41318, 1),  # Savannah Highmane 46204
        (997, 1),  # Savannah Highmane
        (40409, 1),  # Savannah Highmane
        (41076, 1),  # Savannah Highmane
        (38412, 1),  # Savannah Highmane
        (366, 1),  # Savannah Highmane 1086
        (641, 1),  # Savannah Highmane
        (41286, 1),  # Savannah Highmane
        (40906, 1),  # Savannah Highmane
        (41926, 1),  # Savannah Highmane
        (662, 1),  # Savannah Highmane
        (138, 1)  # Savannah Highmane
    )

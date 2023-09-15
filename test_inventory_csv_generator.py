import csv
import json
import pytest
from random import randint 

from inventory_csv_generator import InventoryCsvGenerator
from entry_forms_and_databases import EntryForms

'''
Important:
Run these tests AFTER test_entry_forms_and_databases.py
'''

@pytest.fixture
def inventory_csv_generator():
    inventory_generator = InventoryCsvGenerator()

    return inventory_generator


def _write_mock_set_and_foil_status_form(card_set, foil_status, inventory_format):
    with open(EntryForms.set_and_foil_status_path, "w") as status:
        set_and_status = csv.writer(status)
        set_and_status.writerow((card_set, foil_status, inventory_format))


def _write_mock_collector_number_form(card_range):
    with open(EntryForms.collector_numbers_path, "w") as cards_in_set:
        cn = csv.writer(cards_in_set, delimiter = ".")
        cn.writerow((str(i) for i in card_range))


def _scryfall_test_values(set_abbr):
    with open("scryfall_default-cards.json") as scryfall_object:
        scryfall_json = json.load(scryfall_object)

        def get_card_set():
            for card in scryfall_json:
                if card.get("set") == set_abbr:
                    return card.get("set_name")
        
        card_list = [card.get("name") for card in scryfall_json if card.get("set") == set_abbr]
        card_list.sort()
        card_list_length = len(card_list)
        card_set = get_card_set()

        return (card_list_length, card_list, card_set)


def _set_abbreviation_list():
    with open("scryfall_default-cards.json") as scryfall_object:
        scryfall_json = json.load(scryfall_object)
        abbreviation_set = {card.get("set") for card in scryfall_json}

        return tuple(abbr for abbr in abbreviation_set) 


def _set_foil_status_and_format():
    with open(EntryForms.set_and_foil_status_path) as set_and_status_object:
        info_csv = csv.reader(set_and_status_object)
        card_set, foil_status, inventory_format = next(info_csv)
        
        return (card_set, foil_status, inventory_format)


'''
Call this test using -s flag and make note of the set length. The function gets it's data from the same database that it is tested against using _scryfall_test_values().
Making sure that the set length is correct by doing a simple Google search for how many cards is in the set is a good check that all the cards in the set are indeed in the database. The second assurance is making sure the card names listed in the shown list make sense.
If both these things coorelate then the odds that the database is corrupt is slim. 
'''
def test_get_card_dictionary(inventory_csv_generator):
    scryfall_dict = inventory_csv_generator.get_card_dictionary()
    set_list = _set_abbreviation_list() 

    for set_abbr in set_list:
        card_list = [card.get("name") for card in scryfall_dict if card.get("set") == set_abbr] 
        card_list.sort()
        test_len, test_card_list, card_set = _scryfall_test_values(set_abbr)
        print(f"\nCARDS IN {card_set}\nEXPECTED LENGTH: {test_len}\nCARD LIST:\n{test_card_list}\n")

        assert len(card_list) == test_len 
        assert card_list == test_card_list


def test_generate_upload_csv(inventory_csv_generator):
    set_list = _set_abbreviation_list()
    random_indexes = {randint(0, len(set_list)) for i in range(50)}
    card_dictionary = inventory_csv_generator.get_card_dictionary()
    fetch_card_by_collector_number_and_set = lambda x, y: [card for card in card_dictionary if card.get("collector_number") == x and card.get("set") == y][0]
    inventory_formats = ("cardsphere", "deckbox")

    #Needed because split cards and double sided card names need to be truncated in order to be loaded by your online inventory site. However when those names are checked against the json database directly the assertion will fail. Instead we need to check that the the name from the inventory file is contained inside the name pulled from the Scryfall Database.
    def card_dictionary_check(set_abbr, card_name):
        for card in card_dictionary:
            if card.get("name").find(card_name) != -1 and card.get("set") == set_abbr:
                return card_name
        return f"Card containing {card_name} not found!"

    for inventory_format in inventory_formats:
        for i in random_indexes:
            set_abbr = set_list[i]
            card_list_length, unused_list, card_set = _scryfall_test_values(set_abbr)
            card_range = range(1, card_list_length)
            _write_mock_set_and_foil_status_form(set_abbr, "non-foil", inventory_format)
            _write_mock_collector_number_form(card_range)
            inventory_csv_generator.generate_upload_csv()

            with open(InventoryCsvGenerator.inventory_output_path, "r") as inventory_object:
                inventory_dict = csv.DictReader(inventory_object)
                inventory_format = _set_foil_status_and_format()[2]
            
                for card in inventory_dict:

                    if inventory_format == "cardsphere":
                        assert card.get("Count") == str(1)
                        assert card.get("Name") == card_dictionary_check(set_abbr, card.get("Name"))
                        assert card.get("Expansion") == card_set
                        assert card.get("Foil") == str(0)
                        assert card.get("Condition") == "NM"
                        assert card.get("Language") == "English"
                        assert card.get("Status") == "Have"

                    elif inventory_format == "deckbox":
                        assert card.get("Count") == str(1)
                        assert card.get("Tradelist Count") == str(1)
                        assert card.get("Name") == card_dictionary_check(set_abbr, card.get("Name"))
                        assert card.get("Expansion") == card_set
                        assert card.get("Foil") == str(0)
                        assert card.get("Condition") == "Near Mint"
                        assert card.get("Language") == "English"
                        assert card.get("Card Number") == fetch_card_by_collector_number_and_set(card.get("Card Number"), set_abbr).get("collector_number") 

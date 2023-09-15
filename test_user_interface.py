import pytest
import csv
import json

from user_interface import UserInterface
from entry_forms_and_databases import EntryForms, ScryfallDatabase
from inventory_csv_generator import InventoryCsvGenerator

@pytest.fixture
def ux_object():
    ux_object = UserInterface()
    
    return ux_object


@pytest.fixture
def mercadian_masques_card_names():
    first_fifteen_name_values = ("Afterlife", "Alabaster Wall", "Armistice", "Arrest", "Ballista Squad", "Charm Peddler", "Charmed Griffin", "Cho-Arrim Alchemist", "Cho-Arrim Bruiser", "Cho-Arrim Legate", "Cho-Manno, Revolutionary", "Cho-Manno's Blessing", "Common Cause", "Cornered Market", "Crackdown")

    return first_fifteen_name_values


def _entry_forms_assertions():
    
    with open(EntryForms.set_and_foil_status_path) as set_and_foil_object:
        set_and_foil_csv = csv.reader(set_and_foil_object)
        #This is the same thing we did in the entry_forms_and_databases.py test because we have a natural sentence with commas on a .csv file using a "," delimiter
        set_and_foil_instructions = ",".join(next(set_and_foil_csv))
        new_line_char_index = EntryForms.set_and_foil_instructions.find("\n")

        assert set_and_foil_instructions == EntryForms.set_and_foil_instructions[:new_line_char_index]
        
    with open(EntryForms.collector_numbers_path) as collector_numbers_object:
        collector_numbers_csv = csv.reader(collector_numbers_object)
        collector_numbers_instructions = next(collector_numbers_csv)[0]
        new_line_char_index = EntryForms.collector_numbers_instructions.find("\n")

        assert collector_numbers_instructions == EntryForms.collector_numbers_instructions[:new_line_char_index]


def _scryfall_database_assertions(mercadian_masques_card_names):

    with open(ScryfallDatabase.json_destination) as scryfall_db:
        scryfall_json = json.load(scryfall_db)

        assert list(scryfall_json[0].keys()) == ["collector_number", "name", "set", "set_name"]

        mercadian_masques_first_15 = [card for i in range(1,16) for card in scryfall_json if card.get("set") == "mmq" and card.get("collector_number") == str(i)] 
        
        assert len(mercadian_masques_first_15) == len(mercadian_masques_card_names)

        for card, assertion_name in zip(mercadian_masques_first_15, mercadian_masques_card_names):
            assert card.get("name") == assertion_name
            assert card.get("set") == "mmq"
            assert card.get("set_name") == "Mercadian Masques"


def _fill_entry_forms_for_generate_inventory_test():
    with open(EntryForms.set_and_foil_status_path, "w") as set_and_foil_object:
        set_and_foil_writer = csv.writer(set_and_foil_object)
        set_and_foil_writer.writerow(("MMQ", "non-foil", "cardsphere"))
        
    with open(EntryForms.collector_numbers_path, "w") as collector_numbers_object:
        collector_numbers_writer = csv.writer(collector_numbers_object)
        row_string = ".".join(str(i) for i in range(1,15))
        collector_numbers_writer.writerow(row_string)


def _generate_inventory_assertions(mercadian_masques_card_names):
    with open(InventoryCsvGenerator.inventory_output_path) as inventory_object:
        inventory_dict = csv.DictReader(inventory_object) 

        for card, assertion_name in zip(inventory_dict, mercadian_masques_card_names):
            assert card.get("Count") == "1"
            assert card.get("Name") == assertion_name
            assert card.get("Expansion") == "Mercadian Masques"
            assert card.get("Foil") == "0"
            assert card.get("Condition") == "NM"
            assert card.get("Language") == "English"
            assert card.get("Status") == "Have"


def test_reset_entry_forms(ux_object):
    ux_object._reset_entry_forms()
    _entry_forms_assertions()


def test_download_and_optimize_database(ux_object, mercadian_masques_card_names):
    ux_object._download_and_optimize_database()
    _scryfall_database_assertions(mercadian_masques_card_names)


def test_generate_inventory_csv(ux_object, mercadian_masques_card_names):
    _fill_entry_forms_for_generate_inventory_test()
    ux_object._generate_inventory_csv()
    _generate_inventory_assertions(mercadian_masques_card_names)


def test_expansion_names_tuple(ux_object):
    with open(InventoryCsvGenerator.inventory_output_path) as inventory_object:
        inventory_dict = csv.DictReader(inventory_object)
        expansion_tuple = [(card.get("set"), card.get("set_name")) for card in inventory_dict if card.get("collector_number") == "1"]
        expansion_tuple.sort(key = lambda x: x[1])

        for expansion_tpl, test_tpl in zip(ux_object.expansion_names_tuple, expansion_tuple):
            assert expansion_tpl == test_tpl 



    


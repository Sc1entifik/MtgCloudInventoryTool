import pytest
import csv
import json

from entry_forms_and_databases import EntryForms, ScryfallDatabase

'''
IMPORTANT:
Run these tests BEFORE running test_inventory_csv_generator.py 
'''

@pytest.fixture
def scryfall_database():
    database = ScryfallDatabase()
    return database


@pytest.fixture
def entry_forms():
    entry_forms = EntryForms()
    return entry_forms


def test_reset_entry_forms(entry_forms):
    entry_forms.create_entry_form_instructions()
    
    with open(EntryForms.entry_forms_instructions_path, 'r') as status_object:
        status = csv.reader(status_object)
        #Lines need to be joined back togeither using the ",".join(next(status)) line because of the commas naturally occurring in the sentence and the file being a .csv with a comma delimiter
        status_instructions = ",".join(next(status))
        new_line_index = EntryForms.entry_forms_instructions.find('\n')
        assert status_instructions == EntryForms.entry_forms_instructions[:new_line_index]


def test_get_download_link(scryfall_database):
    comparison_value = "https://data.scryfall.io/default-cards/"
    assert scryfall_database.get_download_link()[:len(comparison_value)] == comparison_value


def test_download_scryfall_database(scryfall_database):
    scryfall_database.download_scryfall_database()

    with open(ScryfallDatabase.json_destination) as scryfall_db:
        scryfall_json = json.load(scryfall_db)
        key_list = [key for key in scryfall_json[0].keys()]
        key_list.sort()
        assert key_list == ['artist', 'artist_ids', 'booster', 'border_color', 'card_back_id', 'cardmarket_id', 'cmc', 'collector_number', 'color_identity', 'colors', 'digital', 'edhrec_rank', 'finishes', 'flavor_text', 'foil', 'frame', 'full_art', 'games', 'highres_image', 'id', 'illustration_id', 'image_status', 'image_uris', 'keywords', 'lang', 'layout', 'legalities', 'mana_cost', 'mtgo_foil_id', 'mtgo_id', 'multiverse_ids', 'name', 'nonfoil', 'object', 'oracle_id', 'oracle_text', 'oversized', 'penny_rank', 'power', 'prices', 'prints_search_uri', 'promo', 'purchase_uris', 'rarity', 'related_uris', 'released_at', 'reprint', 'reserved', 'rulings_uri', 'scryfall_set_uri', 'scryfall_uri', 'set', 'set_id', 'set_name', 'set_search_uri', 'set_type', 'set_uri', 'story_spotlight', 'tcgplayer_id', 'textless', 'toughness', 'type_line', 'uri', 'variation']


def test_optimize_scryfall_database(scryfall_database):
    scryfall_database.optimize_scryfall_database()

    with open(ScryfallDatabase.json_destination) as scryfall_db:
        scryfall_json = json.load(scryfall_db)
        key_list = [key for key in scryfall_json[0].keys()]
        key_list.sort()
        assert key_list == ['collector_number', 'name', 'set', 'set_name']



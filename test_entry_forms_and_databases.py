import pytest
import csv
import json
import gzip

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

    with open(ScryfallDatabase.json_destination, "rb") as compressed_scryfall_db:
        with gzip.GzipFile(fileobj=compressed_scryfall_db, mode="rb") as scryfall_cards:
            magic_cards = (json.loads(line) for line in scryfall_cards)
            magic_card = next(magic_cards)
            key_list = [key for key in magic_card.keys()]
            print(key_list)
            # Assertion value may change from time to time due to the API. This value needs to be re hard coded when the print(key_list) doesn't match the assertion value but the list seems legitimate. 
            assertion_value = ['object', 'id', 'oracle_id', 'multiverse_ids', 'mtgo_id', 'arena_id', 'tcgplayer_id', 'cardmarket_id', 'name', 'lang', 'released_at', 'uri', 'scryfall_uri', 'layout', 'highres_image', 'image_status', 'image_updated_at', 'image_uris', 'mana_cost', 'cmc', 'type_line', 'oracle_text', 'colors', 'color_identity', 'keywords', 'produced_mana', 'all_parts', 'legalities', 'games', 'reserved', 'game_changer', 'foil', 'nonfoil', 'finishes', 'oversized', 'promo', 'reprint', 'variation', 'set_id', 'set', 'set_name', 'set_type', 'set_uri', 'set_search_uri', 'scryfall_set_uri', 'rulings_uri', 'prints_search_uri', 'collector_number', 'digital', 'rarity', 'card_back_id', 'artist', 'artist_ids', 'illustration_id', 'border_color', 'frame', 'full_art', 'textless', 'booster', 'story_spotlight', 'prices', 'related_uris', 'purchase_uris'] 

            assert key_list == assertion_value


def test_optimize_scryfall_database(scryfall_database):
    scryfall_database.optimize_scryfall_database()

    with open(ScryfallDatabase.json_destination) as scryfall_db:
        scryfall_json = json.load(scryfall_db)
        key_list = [key for key in scryfall_json[0].keys()]
        key_list.sort()
        assert key_list == ['collector_number', 'name', 'set', 'set_name']



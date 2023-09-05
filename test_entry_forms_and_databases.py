import pytest
import csv
import json

from entry_forms_and_databases import EntryForms, ScryfallDatabase

@pytest.fixture
def scryfall_database():
    database = ScryfallDatabase()
    return database


@pytest.fixture
def entry_forms():
    entry_forms = EntryForms()
    return entry_forms


def test_reset_entry_forms(entry_forms):
    entry_forms.reset_entry_forms()
    
    with open(EntryForms.set_and_foil_status_path, 'r') as status_object:
        status = csv.reader(status_object)
        status_instructions = next(status)[0]
        new_line_index = EntryForms.set_and_foil_instructions.find('\n')
        assert status_instructions == EntryForms.set_and_foil_instructions[:new_line_index]

    with open(EntryForms.collector_numbers_path, 'r') as collector_number_object:
        cn = csv.reader(collector_number_object)
        cn_instructions = next(cn)[0]
        new_line_index = EntryForms.collector_numbers_instructions.find('\n')
        assert cn_instructions == EntryForms.collector_numbers_instructions[:new_line_index]
        

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



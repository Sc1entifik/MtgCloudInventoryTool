import pytest
import csv
import json

from entry_forms_and_databases import EntryForms, ScryfallDatabase

def test_reset_entry_forms():
    ef = EntryForms()
    ef.reset_entry_forms()
    
    with open(EntryForms.set_and_foil_status_path, 'r') as status_object:
        status = csv.reader(status_object)
        status_header = next(status)
        assert status_header == []

    with open(EntryForms.collector_numbers_path, 'r') as collector_number_object:
        cn = csv.reader(collector_number_object)
        cn_header = next(cn)
        assert cn_header == []


def test_download_scryfall_database():
    db = ScryfallDatabase
    db.download_scryfall_database()

    with open(db.scryfall_database_path) as scryfall_db:
        scryfall_json = json.load(scryfall_db)
        key_list = [key for key in scryfall_json[0].keys()]
        key_list.sort()
        assert key_list == ['collector_number', 'name', 'set', 'set_name']

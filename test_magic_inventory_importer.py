import csv
import json

from magic_inventory_generator import MagicInventoryGenerator
from entry_forms_and_databases import EntryForms


def _write_mock_set_and_foil_status_form(set, foil_status):
    with open(EntryForms.set_and_foil_status_path, w) as status:
        set_and_status = csv.writer(status)
        set_and_status.write(set,foil_status)

def _write_mock_collector_number_form():
    with open(EntryForms.collector_number_path, w) as first_fifty:
        cn = csv.writer(first_fifty)
        cn.write(".".join(str(i) for i in range(1, 51)))



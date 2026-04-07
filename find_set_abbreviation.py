import json
from entry_forms_and_databases import ScryfallDatabase

def find_set_abbreviation(set_name):
    with open(ScryfallDatabase.json_destination) as scyfall_object:
        scyfall_dictionary = json.load(scyfall_object)

    for obj in scyfall_dictionary:
        if obj.get("set_name"):
            formatted_set_name = obj.get("set_name").lower()
            if formatted_set_name == set_name.lower():
                return obj.get("set") 

    return "You likely spelled the set wrong."

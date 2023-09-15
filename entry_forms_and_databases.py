import csv
import json
import requests

class EntryForms():
    set_and_foil_status_path = "EntryForms/set_and_foil_status.csv"
    collector_numbers_path = "EntryForms/collector_numbers.csv"
    set_and_foil_instructions = "Replace me with a set abbreviation, foil or non-foil, and inventory format like this.\nMMQ,non-foil,cardsphere   (As of now formats include cardsphere, and deckbox)"
    collector_numbers_instructions = "Replace me with collector numbers from the bottom center of your cards separated by periods like this.\n95.75.16.78.116"

    def reset_entry_forms(self):
        with open(EntryForms.set_and_foil_status_path, "w") as set_and_foil:
            set_and_foil.write(EntryForms.set_and_foil_instructions)

        with open(EntryForms.collector_numbers_path, "w") as collector_numbers:
            collector_numbers.write(EntryForms.collector_numbers_instructions)


class ScryfallDatabase():
    scryfall_bulk_data_url = "https://api.scryfall.com/bulk-data"
    json_destination = "scryfall_default-cards.json"
    

    def __init__(self):
        self.scryfall_download_link = self.get_download_link()


    def get_download_link(self):
        download_directory = requests.get(ScryfallDatabase.scryfall_bulk_data_url)
        download_dict = download_directory.json()

        for archive in download_dict.get("data"):
            if archive.get("type") == "default_cards":
                download_url = archive.get("download_uri")
                download_directory.close()
                return download_url


    def download_scryfall_database(self):
        scryfall_json = requests.get(self.scryfall_download_link)

        with open(ScryfallDatabase.json_destination, "wb") as destination_file:
            destination_file.write(scryfall_json.content)
            print(f"{ScryfallDatabase.json_destination} has been created!")
            scryfall_json.close()


    def optimize_scryfall_database(self):

        with open(ScryfallDatabase.json_destination) as scryfall_db:
            scryfall_json = json.load(scryfall_db)
            optimized_key_list = ["collector_number", "name", "set", "set_name"]
            optimized_list = [{key : archive.get(key) for key in optimized_key_list} for archive in scryfall_json]
        
        with open(ScryfallDatabase().json_destination, "w") as scryfall_db:
            scryfall_db.write(json.dumps(optimized_list))
            print(f"{ScryfallDatabase.json_destination} has been optimized for maximum performance!")


import json
import gzip
import requests
from pathlib import Path

class EntryForms():
    entry_forms_directory = "EntryForms"
    entry_forms_instructions_path = "EntryForms/instructions.csv"
    entry_forms_instructions = "Create a file for each set you are bulk importing with the name being the set_abb.csv (example: mmq.csv).\n\nThe first line of each file should have foil or non-foil, and the inventory format (As of now formats include cardsphere, and deckbox) example: non-foil,deckbox\n\nThe second line of each file should be the collector numbers of each card separated by a decimal point. example: 95.75.16.78.116\n\n Once you fill out a file for all sets you are bulk importing run the program and choose option 4 from the main menu. This will create a bulk output file for each entry form you filled out."

    def create_entry_form_instructions(self):
        with open(EntryForms.entry_forms_instructions_path, "w") as set_and_foil:
            set_and_foil.write(EntryForms.entry_forms_instructions)

    def entry_form_file_path_objects(self):
        return Path(EntryForms.entry_forms_directory)

class ScryfallDatabase():
    scryfall_bulk_data_url = "https://api.scryfall.com/bulk-data"
    scryfall_bulk_data_headers = {"User-Agent":"MTG Cloud Inventory Tool", "Accept": "*/*"}
    json_destination = "scryfall_default-cards.json"
    

    def __init__(self):
        self.scryfall_download_link = self.get_download_link()


    def get_download_link(self):
        download_directory = requests.get(ScryfallDatabase.scryfall_bulk_data_url, headers=ScryfallDatabase.scryfall_bulk_data_headers)
        download_dict = download_directory.json()

        for archive in download_dict.get("data"):
            if archive.get("type") == "default_cards":
                download_url = archive.get("jsonl_download_uri")
                download_directory.close()
                return download_url


    def download_scryfall_database(self):
        download_link = self.get_download_link()
        scryfall_json = requests.get(download_link)
        print("This is a large file this might take several minutes.")
        with open(ScryfallDatabase.json_destination, "wb") as destination_file:
            destination_file.write(scryfall_json.content)
            print(f"{ScryfallDatabase.json_destination} has been created!")
            scryfall_json.close()


    def optimize_scryfall_database(self):
        with open(ScryfallDatabase.json_destination, "rb") as compressed_scryfall_db:
            with gzip.GzipFile(fileobj=compressed_scryfall_db, mode="rb") as scryfall_cards:
                magic_cards = (json.loads(line) for line in scryfall_cards)
                optimized_key_list = ["collector_number", "name", "set", "set_name"]
                optimized_card_list = [{key: card.get(key) for key in optimized_key_list} for card in magic_cards]
                
        
        with open(ScryfallDatabase.json_destination, "w") as scryfall_db:
            json.dump(optimized_card_list, scryfall_db)
            print(f"{ScryfallDatabase.json_destination} has been optimized for maximum performance!")

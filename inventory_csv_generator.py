import json
import csv

from entry_forms_and_databases import EntryForms, ScryfallDatabase

class InventoryCsvGenerator():
    inventory_output_path = "InventoryOutput/inventory_upload.csv"
    inventory_header = ("Count", "Name", "Expansion", "Foil", "Condition", "Language", "Status")

    
    def __init__(self):
        self.card_dictionary = self.get_card_dictionary()
    

    def _set_and_foil_status(self):
        with open(EntryForms.set_and_foil_status_path) as set_foil_status_object:
            set_and_foil = csv.reader(set_foil_status_object)
            card_set, foil_status = next(set_and_foil)
            foil_status_conversion = 0 if foil_status == "non-foil" else 1

        return (card_set, foil_status_conversion) 


    def _collector_number_list(self):
        with open(EntryForms.collector_numbers_path) as collector_number_object:
            collector_number_generator = csv.reader(collector_number_object, delimiter = ".")
            collector_number_list = next(collector_number_generator)
            

        return collector_number_list


    def _target_card(self, collector_number, card_set):
        for card in self.card_dictionary:
            if card.get("collector_number") == collector_number and card.get("set") == card_set.lower():
                return card


    def get_card_dictionary(self):
        with open(ScryfallDatabase.json_destination) as scryfall_object:
            scryfall_dictionary = json.load(scryfall_object)
        
        return scryfall_dictionary

    
    def generate_upload_csv(self):
        card_set, foil_status = self._set_and_foil_status()
        collector_numbers = self._collector_number_list()

        with open(InventoryCsvGenerator.inventory_output_path, "w") as inventory_object:
            inventory_csv = csv.writer(inventory_object)
            inventory_csv.writerow(InventoryCsvGenerator.inventory_header)

            for collector_number in collector_numbers:
                target_card = self._target_card(collector_number, card_set)
                
                if target_card:
                    filter_index = target_card.get("name").find("//")
                    #Name filtered for double sided card names since Card Sphere will reject a full double sided card name.
                    filtered_name = target_card.get("name") if filter_index == -1 else target_card.get("name")[:filter_index]
                    inventory_row = (1, filtered_name, target_card.get("set_name"), foil_status, "NM", "English", "Have") 
                    inventory_csv.writerow(inventory_row)
        
        print(f"{InventoryCsvGenerator.inventory_output_path} has been written!\nCheck for accuracy before uploading to your inventory.")





import json
import csv
from pathlib import Path

from entry_forms_and_databases import EntryForms, ScryfallDatabase
from inventory_formats_and_headers import InventoryFormatsAndHeaders

class InventoryCsvGenerator():
    inventory_output_path = "InventoryOutput/"
    
    def __init__(self):
        self.card_dictionary = self.get_card_dictionary()


    def _foil_status_conversion(self, foil_status, inventory_format):
        if inventory_format != "cardnexus":
            return 0 if foil_status == "non-foil" else 1

        else:
            return "Standard" if foil_status == "non-foil" else "Foil"


    def _set_and_foil_status(self, file_path_object):
        card_set = file_path_object.stem

        with open(file_path_object) as set_foil_status_object:
            set_and_foil = csv.reader(set_foil_status_object, delimiter=".")
            foil_status, inventory_format = next(set_and_foil)
            foil_status_conversion = self._foil_status_conversion(foil_status, inventory_format) 

        return (card_set.strip(), foil_status_conversion, inventory_format.strip()) 


    def _collector_number_list(self, file_path_object):
        with open(file_path_object) as collector_number_object:
            collector_number_generator = csv.reader(collector_number_object, delimiter=".")
            next(collector_number_generator) # gets rid of first line of csv file to get to collector numbers
            collector_number_list = next(collector_number_generator)

        return collector_number_list


    def _target_card(self, collector_number, card_set):
        for card in self.card_dictionary:
            if card.get("collector_number") == collector_number and card.get("set") == card_set.lower():
                return card

    
    def _generate_upload_csv(self, file_path_object):
        card_set, foil_status, inventory_format = self._set_and_foil_status(file_path_object)
        collector_numbers = self._collector_number_list(file_path_object)
        formats_and_headers_object = InventoryFormatsAndHeaders()
        headers_by_format = formats_and_headers_object.headers_by_format_dictionary() 
        full_output_path = InventoryCsvGenerator.inventory_output_path + f"{card_set}.csv"

        with open(full_output_path, "w") as inventory_object:
            inventory_csv = csv.writer(inventory_object)
            inventory_csv.writerow(headers_by_format.get(inventory_format))

            for collector_number in collector_numbers:
                target_card = self._target_card(collector_number, card_set)

                
                if target_card:
                    filter_index = target_card.get("name").find("//")
                    #Name filtered for double sided card names since Card Sphere will reject a full double sided card name.
                    filtered_name = target_card.get("name") if filter_index == -1 else target_card.get("name")[:filter_index]
                    inventory_rows_by_format = formats_and_headers_object.inventory_rows_by_format_dictionary(filtered_name, target_card, foil_status, collector_number) 
                    inventory_row = inventory_rows_by_format.get(inventory_format) 
                    inventory_csv.writerow(inventory_row)
        
        print(f"{full_output_path} has been written!\nCheck for accuracy before uploading to your inventory.")


    def _generate_concatenation_header(self):
        entry_forms_files = list(Path(EntryForms.entry_forms_directory).glob("*.csv"))
        inventory_formats_object = InventoryFormatsAndHeaders()
        inventory_header_dict = inventory_formats_object.headers_by_format_dictionary() 
        with open(entry_forms_files[0], "r") as header_form:
            reader = csv.reader(header_form, delimiter=".")
            header = next(reader)
            inventory_format = header[1]

            return inventory_header_dict.get(inventory_format)


    def get_card_dictionary(self):
        with open(ScryfallDatabase.json_destination) as scryfall_object:
            scryfall_dictionary = json.load(scryfall_object)
        
        return scryfall_dictionary


    def generate_upload_csv_files(self):
        entry_forms = EntryForms()
        entry_form_file_objects = entry_forms.entry_form_file_path_objects()

        for file_object in entry_form_file_objects.glob("*.csv"):

            try:
                print(f"PROCESSING: {file_object}")
                self._generate_upload_csv(file_object)
                print()

            except:
                print(f"PROCESSING FAILED: {file_object}")
                print()
                raise


    def concatenate_upload_csv_files(self):
        output_dir = Path(InventoryCsvGenerator.inventory_output_path)
        concatenation_header = self._generate_concatenation_header()
        concatenation_file = output_dir / "concatenation_output.csv"

        with open(concatenation_file, "w") as new_concat:
            writer = csv.writer(new_concat)
            writer.writerow(concatenation_header)

        for output_file_object in output_dir.glob("*.csv"):
            if output_file_object.name == "concatenation_output.csv":
                continue

            with output_file_object.open() as output_file:
                reader = csv.reader(output_file)
                next(reader) # Removing header from each output file.

                with open(concatenation_file, "a") as current_concat:
                    writer = csv.writer(current_concat)
                    writer.writerows(reader)

        print(f"Output files have been concatenated to {concatenation_file}")


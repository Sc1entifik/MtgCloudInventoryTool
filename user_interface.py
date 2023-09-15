import json

from entry_forms_and_databases import EntryForms, ScryfallDatabase
from inventory_csv_generator import InventoryCsvGenerator

class UserInterface:

    def __init__(self):
        self.expansion_names_tuple = self._create_expansion_names_tuple()
        self.user_interface_menu = self._create_user_interface_menu()

    
    def _reset_entry_forms(self):
        entry_forms = EntryForms()
        entry_forms.reset_entry_forms()


    def _download_and_optimize_database(self):
        scryfall_db = ScryfallDatabase()
        scryfall_db.download_scryfall_database()
        scryfall_db.optimize_scryfall_database()

    def _generate_inventory_csv(self):
        inventory_generator = InventoryCsvGenerator()
        inventory_generator.generate_upload_csv()


    def _create_expansion_names_tuple(self):

        with open(ScryfallDatabase.json_destination) as database_object:
            scryfall_dictionary = json.load(database_object)
            expansion_tuple = tuple((card.get("set"), card.get("set_name")) for card in scryfall_dictionary if card.get("collector_number") == "1")
        
        return expansion_tuple


    def _display_instructions(self):
        print("\n\nWelcome to MTG Cloud Inventory Tool. This tool was created to make it easy to cloud inventory your collection using websites such as Deckbox or CardSphere among others.\n\nStep 1: Reset your entry forms. This is comprised of two files that live in an EntryForms folder that are in this code repository. You can either do this manually or through option 2 of this menu.\nStep 2: Download and optimize Scryfall database. Simply choose option 3 from the menu and the Scryfall database will be downloaded and then optimized for this use case. You only need to do this if you have not done so already or if a new expansion has been released and you need to update the database so it has all the new cards in it.\nStep 3: Fill out the entry forms. Use your favorite text editor and fill out the .csv files that you reset from Step 1. If you used option 2 to complete Step 1 then the file will have a set of instructions inside of it to follow. Remember that the collector_numbers.csv file needs to separate the card values with a period and not a comma like so 12.34.53.122\nStep 4: Generate the inventory_upload.csv file by choosing option 4. If you followed these instructions faithfully up to this point you should have an inventory_upload.csv file in the InventoryOutput folder of this code repository. Check it for accuracy and then upload it to wherever you cloud inventory your cards.\n\n\n\nTIPS:\n1) If you want to upload multiple files at once after you generate one go ahead and rename it to something else other than inventory_upload.csv such as draft.csv for example. The program will always write or rewrite the file named inventory_upload.csv in the InventoryOuptut folder.\n2) If the cloud website gives you formats you can choose from and you see anything referring to CardSphere or Deckbox format choose one of those as those are the supported .csv formats with this program.\n3) If your web inventory service or program doesn't work with this format let me know what format they need to be in and I will try to include that in a future version. You can also feel free to play with this codebase and roll your own as long as you don't try to claim my codebase as your own.\n\n")


    def _create_user_interface_menu(self):
        user_interface_menu = {
            1 : self._display_instructions,
            2 : self._reset_entry_forms,
            3 : self._download_and_optimize_database,
            4 : self._generate_inventory_csv,
            5 : None
        }

        return user_interface_menu


    def generate_main_menu(self):
        menu_input = input("\nMTG Cloud Inventory Tool Main Menu\nPlease choose one of the following numbered options.\n1) Detailed Instructions\n2) Reset Entry Forms\n3) Update And Optimize Card Database\n4) Generate Inventory Upload File\n5) Quit\n\n")

        try:
            if menu_input == "5":
                return

            else:
                selected_option = self.user_interface_menu.get(int(menu_input))
                selected_option()
                return self.generate_main_menu()

        except (ValueError, TypeError):
            print("\n\nPlease enter a valid number input from the main menu.\n\n")
            return self.generate_main_menu()
        


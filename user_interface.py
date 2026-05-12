import json

from entry_forms_and_databases import EntryForms, ScryfallDatabase
from inventory_csv_generator import InventoryCsvGenerator
from find_set_abbreviation import find_set_abbreviation

class UserInterface:

    def __init__(self):
        self.expansion_names_tuple = self._create_expansion_names_tuple()
        self.user_interface_menu = self._create_user_interface_menu()

    
    def _create_entry_form_instructions(self):
        entry_forms = EntryForms()
        entry_forms.create_entry_form_instructions()


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
        print("\n\nWelcome to MTG Cloud Inventory Tool. This tool was created to make it easy to cloud inventory your collection using websites such as Deckbox or CardSphere among others.\n\nStep 1: Download and optimize Scryfall database. Simply choose option 3 from the menu and the Scryfall database will be downloaded and then optimized for this use case. You only need to do this if you have not done so already or if a new expansion has been released to get all the new cards to the database.\n\nStep 2: Fill out entry forms. Choose option 2 of this menu Create Entry Form Instructions which will create a file in the EntryForms folder which will tell you how to create and fill out entry forms for each set you want to bulk import. \n\nStep 3: Generate the inventory_upload.csv file by choosing option 4 of this menu. Assuming you filled out all your forms correctly you should now have a file in InventoryOutput for each file you entered in EntryForms. You can now upload this to a cloud inventory website of your choosing.\n\n\n\nTIPS:\n1) If the cloud website gives you formats you can choose from and you see anything referring to CardSphere or Deckbox format choose one of those as those are the supported .csv formats with this program.\n3) If your web inventory service or program doesn't work with this format let me know what format they need to be in and I will try to include that in a future version. You can also feel free to play with this codebase and roll your own as long as you don't try to claim my codebase as your own.\n\n")


    def _set_abbr_finder(self):
        print("")
        print(find_set_abbreviation(input("Enter the name of the set.\n")))


    def _create_user_interface_menu(self):
        user_interface_menu = {
            1 : self._display_instructions,
            2 : self._create_entry_form_instructions,
            3 : self._download_and_optimize_database,
            4 : self._generate_inventory_csv,
            5 : self._set_abbr_finder,
            6 : None
        }

        return user_interface_menu


    def generate_main_menu(self):
        menu_input = input("\nMTG Cloud Inventory Tool Main Menu\nPlease choose one of the following numbered options.\n1) Detailed Instructions\n2) Create Entry Form Instructions\n3) Update And Optimize Card Database\n4) Generate Inventory Upload File\n5) Set Abbreviation By Set Name\n6) Quit\n\n")

        try:
            if menu_input == "6":
                return

            else:
                selected_option = self.user_interface_menu.get(int(menu_input))
                selected_option()
                return self.generate_main_menu()

        except (ValueError, TypeError):
            print("\n\nPlease enter a valid number input from the main menu.\n\n")
            return self.generate_main_menu()
        


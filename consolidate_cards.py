import csv

class ConsolidateCards():

    def __init__(self, inventory_path):
        self.inventory_path = inventory_path
        self.headers = [] 
        self.current_inventory = self._get_current_card_inventory()
        self.card_count_dictionary = self._get_card_count_dictionary()
        self.consolidated_dictionary = self._get_consolidated_dictionary()

    def _get_current_card_inventory(self):
        with open(self.inventory_path, "r") as inventory_file:
            card_inventory = csv.DictReader(inventory_file)
            self.headers = card_inventory.fieldnames
            return list(card_inventory)

    def _get_card_count(self, card):
        count = 0

        for inventory_card in self.current_inventory:
            if self._same_card(card, inventory_card):
                count += 1

        return count

    def _same_card(self, card1, card2):
        same_card = True
        fields = card1.keys()

        for field in fields:
            if card1.get(field) != card2.get(field):
                same_card = False
                
        return same_card

    def _get_card_count_dictionary(self):
        return {tuple(sorted(card.items())): self._get_card_count(card) for card in self.current_inventory}

    def _get_consolidated_dictionary(self):
        consolidated_dictionary = [{key: value for key, value in card_tuple} for card_tuple in self.card_count_dictionary.keys()]

        for card in consolidated_dictionary:
            card["Count"] = self.card_count_dictionary.get(tuple(sorted(card.items())))

        return [{header: card.get(header) for header in self.headers} for card in consolidated_dictionary]

    def consolidate_inventory(self):
        with open(self.inventory_path , "w") as inventory_file:
            writer = csv.DictWriter(inventory_file, fieldnames=self.headers)
            writer.writeheader()
            writer.writerows(self.consolidated_dictionary)



test_inventory = ConsolidateCards("InventoryOutput/concatenation_output.csv")
test_inventory.consolidate_inventory()

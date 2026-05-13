class InventoryFormatsAndHeaders():
    supported_inventory_formats = ("cardsphere", "deckbox", "cardsphere")
    inventory_headers = ( ("Count", "Name", "Expansion", "Foil", "Condition", "Language", "Status"), ("Count", "Tradelist Count", "Name", "Expansion", "Foil", "Condition", "Language", "Card Number"), ("Count", "Tradelist Count", "Name", "Expansion", "Foil", "Condition", "Language", "Card Number") )


    def headers_by_format_dictionary(self):
        return {key:value for key, value in zip(InventoryFormatsAndHeaders.supported_inventory_formats, InventoryFormatsAndHeaders.inventory_headers)}

    
    def inventory_rows_by_format_dictionary(self, filtered_name, target_card, foil_status, collector_number):
        inventory_rows_in_format_order = ( (1, filtered_name, target_card.get("set_name"), foil_status, "NM", "English", "Have"), (1, 1, filtered_name, target_card.get("set_name"), foil_status, "Near Mint", "English", collector_number), (1, 1, filtered_name, target_card.get("set_name"), foil_status, "Near Mint", "English", collector_number) )
        
        return {key:value for key, value in zip(InventoryFormatsAndHeaders.supported_inventory_formats, inventory_rows_in_format_order)}


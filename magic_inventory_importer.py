'''
To Do:
    1) Refactor code organized as a class.
        a. Keep working towards this great job so far!
        b. Update ternary expressions inside row_data for create_inventory_import_files method to include borderless cards and promo pack cards.


    2) Create function which automatically installs updated versions of scryfall_mtg.json then rewrites it to a json that doesn't suck and has only the needed key value pairs!
        a. This should be the final step in this program. Once finished though the program will be ready for deployment on github.
    
    3) Create some user interfaces.
        a. First create a text base user interface with menus which runs in the terminal
        b. Create a web based user interface using Django.

Program Description:
The pucaporter program allows you to easily take large lists of cards and quickly reference them by their print number and be returned csv files which can be imported directly to your Card Sphere inventory!
'''

import os
import csv 
import json


def create_data_input_forms():
    card_types = ('foil','','alt_art_foil','alt_art','borderless','borderless_foil','promo_pack','promo_pack_foil')
    
    with open(MagicInventoryImporter.input_form_path.format('magic_set.csv'),'w') as set_form:
        writer = csv.writer(set_form)
        writer.writerow([])

    
    for label in card_types:
        with open(MagicInventoryImporter.input_form_path.format('card_list_{}.csv'.format(label)),'w') as number_form:
            writer = csv.writer(number_form)
            writer.writerow([])

    return 'Data entry forms have been created in ./EntryForms/ !'


class MagicInventoryImporter():

    input_form_path = './EntryForms/{}'
    output_form_path = './InventoryOutput/{}'
    input_form_directory = os.listdir(input_form_path.format(''))


    def __init__(self):
        self.card_list_dictionary = self.return_input_form_dictionary()
        self.card_set = self.card_list_dictionary.pop('magic_set.csv')[0].lower()


    def return_input_form_dictionary(self):
        input_form_dictionary = {}

        for name in MagicInventoryImporter.input_form_directory:
            with open(MagicInventoryImporter.input_form_path.format(name),'r') as data:
                reader = csv.reader(data,delimiter = '.')
                input_form_dictionary[name] = next(reader)
        
        return input_form_dictionary 
    

    def create_inventory_import_files(self,condition = 'NM',language = 'English', status ='Have'):
        
        scryfall_dict = self.return_scryfall_dict()
        
        header = ['Count','Name','Expansion','Foil','Condition','Language','Status']
        row_values = ([[1,scryfall_dict.get(collector_number),scryfall_dict.get(self.card_set) if card_list.find('_alt_art') == -1 else scryfall_dict.get(self.card_set) +' - Showcase',0 if card_list.find('_foil.csv') == -1 else 1,condition,language,status] for collector_number in self.card_list_dictionary.get(card_list) ] for card_list in self.card_list_dictionary.keys())
        import_file_dict = {key:value for key,value in zip(self.card_list_dictionary.keys(),row_values)}
        
        for file_name in import_file_dict:
            with open(MagicInventoryImporter.output_form_path.format(file_name),'w') as import_file:
                writer = csv.writer(import_file)
                writer.writerow(header)
                writer.writerows(import_file_dict.get(file_name))
        
        return '{} files have been written to {}!'.format(import_file_dict.keys(),MagicInventoryImporter.output_form_path)
    

    def return_wanted_json_dict_list(self):
        wanted_scryfall_dict_list = []

        with open('scryfall_mtg.json','r') as scryfall_object:
            scryfall_dict_list = json.loads(scryfall_object.read())
            
            for dictionary in scryfall_dict_list:
                #needed in order to get Card Sphere to accept your .csv files otherwise you get an import error because of the double slash in name
                remove_double_sided = dictionary.get('name') if dictionary.get('name').find('//') == -1 else dictionary.get('name')[0:dictionary.get('name').find('//')]
                wanted_scryfall_dict_list.append({'set':dictionary.get('set'), 'set_name':dictionary.get('set_name'), 'collector_number':dictionary.get('collector_number'), 'name':remove_double_sided})

        return wanted_scryfall_dict_list


    def rewrite_scryfall_json(self):
        wanted_scryfall_dict_list = self.return_wanted_json_dict_list()

        with open('sample.json','w') as file:
            json.dump(wanted_scryfall_dict_list,file) 

        return 'sample.json database file written!'


    def return_scryfall_dict(self):
        with open('sample.json','r') as scryfall:
            scryfall_dict_list = json.loads(scryfall.read())
            return_scryfall_dict = {}

            for dictionary in scryfall_dict_list:
                if dictionary.get('set') == self.card_set:
                    return_scryfall_dict.update({self.card_set:dictionary.get('set_name')})
                    break
                           
            for dictionary in scryfall_dict_list:
                if dictionary.get('set') == self.card_set:
                    return_scryfall_dict.update({dictionary.get('collector_number'):dictionary.get('name')})

        return return_scryfall_dict


draft_importer = MagicInventoryImporter() 
print(draft_importer.create_inventory_import_files())

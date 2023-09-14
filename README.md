# MTG Cloud Inventory Tool  

## Create A Perfect Cloud Inventory Of Your Magic Cards 
This python based tool will allow you to quickly create and maintain a cloud based inventory of your MTG cards when used with a site like Card Sphere or Deckbox.

## How This Tool Works
This tool will use a .csv file containing the set abbreviation, foil status, and then  another .csv file containing collector numbers that are on the bottom of every magic card to create a .csv file filling out all the details you need to upload those cards to your inventory on sties like Card Shpere or Deckbox. Using this tool to upload a large or even medium sized collection of cards down to all your commons takes minutes.

## Instructions
1) Run mtg_cloud_inventory_tool.py from the command line.
2) Check out the instructions from the UX in there.
3) Make sure to fill out collector_numbers.py in EntryForms folder separating the card numbers with periods like so 12.53.214.321 and not commas.
4) After generating file upload it to your inventory service through their .csv file upload option.

## Common Use Cases
- Mainining your inventory after a draft or sealed deck.
- Buying other bulk card collections.
- Selling bulk cards from your collection.
- Checking card wanted lists online against your collection.

## Versions
- 0.01 - First commit. This was one of the first projects that I built before I knew how to use version control and was still learning the basics of OOP. Sorry for the hard to read code but I had to learn somehow. While the project works I didn't want to leave it in it's current condition. This will soon be fixed starting with tests and refactoring. I am also going to break up this code base some more making it easier to read. Please wait for a later version to use. I will have this unknotted soon.

- 0.03 - entry_forms_and_databases.py and test_entry_forms_and_databases.py written and passed. 

- 0.5 - inventory_csv_generator.py and test_inventory_csv_generator.py written and passed. Old files removed from repository.

- 1.0 - user_interface.py, test_user_interface.py, and mtg_cloud_inventory_tool.py have been created. The text based UX is here! This is nothing fancy but definitely sufficient for this use case.



## Coming Soon
Improvements to text based UX such as ASCII art.

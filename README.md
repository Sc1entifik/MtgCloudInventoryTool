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

### Formats and Deckbox Now Supported
As of version 1.2 I was made aware that CardSphere is sadly ending it's service. This made me want to find a new cloud inventory site to focus this project through. I ended up going with Deckbox. While both Puca Trade and CardSpherewere fundamentally different trading platforms centralizing around market place style selling and buying cards through points systems instead of direct trading there now seems to be no other platform that fills that gap any longer. Deckbox however does fill the cloud inventory functions that we were used to from Puca Trade and CardSphere and does support trading although directly using cards via card for card. This will have to do until another platform steps up to fill this gap.

### Lemonade From The Lemons
While I loved Puca Trade, found CardSphere just tollerable, and not a fan of Deckbox there are some improvements in using the Deckbox .csv formatting. The big one is that it allows you to track the collector_number of the cards so your textless and showcase cards are automatically inventoried with no special treatment. You can also inventory your cards down to basic lands! The tool not being able to differentiate between special art cards was an ugly little bug that just went away. 

To see the new instructions on how to choose between cardsphere and deckbox format reset the entry forms using option 2 of the mtg_cloud_inventory.py tool. Open that file and read it to see the new instructions. The only thing that really changed here is after adding your foil status in set_and_foil_status.csv fowllow that with a comma then specify either deckbox or cardsphere. **example: MMQ,non-foil,deckbox** 

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

- 1.2 - Better support for Deckbox added! After getting the news that CardSphere was ending I decided to add more Deckbox focused support. You can now choose between cardsphere and deckbox in the set_and_foil_status.csv file. This also makes the program agnositic to adding showcase and textless card art cards when using deckbox format. Use option 2 in the mtg_cloud_inventory tool then read the new instructions written in the set_and_voil_status.csv file for the new instructions.

## Coming Soon
Improvements to text based UX such as ASCII art.

## Licensing Stuff
This project is designed for personal use for people with personal card collections. It is not intended to be part of any commercial software or SAS type thing. That being said I don't really care too much what you use this code base for as long as it is non-commercial in nature and you assume all responsibility in using it. I just ask for proper credit where credit is due if you use this in your coding project somewhere. 

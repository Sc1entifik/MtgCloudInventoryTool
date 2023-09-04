# MTG Cloud Inventory Tool  

## Create A Perfect Cloud Inventory Of Your Magic Cards 
This python based tool will allow you to quickly create and maintain a cloud based inventory of your MTG cards when used with a site like Card Sphere or Deckbox.

## How This Tool Works
This tool will take a .csv list cointaining the set abbreviation and collector numbers that are on the bottom of every magic card then create a .csv file filling out all the details you need to upload those cards to your inventory on sties like Card Shpere or Deckbox. Using this tool uploading a large or even medium sized collection of cards down to all your commons takes minutes.

## Instructions
1) Make sure the scryfall.json file is updated to the newest release so it contains all magic cards you would want to import. This needs to be done every time WOTC releases a new set. This codebase should automate this process for you soon!
2) Run the optimizer method to create an optimized version of scryfall.json so that it only contains the information we need thus dramatically increasing performance of the app.
3) Run the renew_input_forms_method to either create or overwrite old input forms in the entry forms folder.
4) Separate all your cards by set and foil/nonfoil then place them in large piles. At this point do not bother sorting them by rarity, or even color.
5) Go to the EntryForms folder then go to set_and_foil_status.csv. Enter the set abbreviation separated by a comma followed by either foil or non-foil.
6) Go to collector_numbers.csv. Here you will enter the collector numbers that are on the bottom of each card. Separate each three digit collector number with a period. *example: 115.61.12.78.93* This makes it easy and fast to enter the numbers only using the number pad on the right side of the keyboard.
7) Run the generate_inventory_csv method. This will generate you an inventory.csv file. Open this file and check it to make sure it looks correct. 
8) Once you are satisfied with your file go to the upload section of your Card Sphere or Deckbox website and upload the .csv file and it will add those cards to your online inventory!
9) Put the now inventoried cards away any way you like.
10) Repeat steps 3-10 for all other cards not yet inventoried.

## Common Use Cases
- Mainining your inventory after a draft or sealed deck.
- Buying other bulk card collections.
- Selling bulk cards from your collection.
- Checking card wanted lists online against your collection.

## Versions
- 0.01 First commit. This was one of the first projects that I built before I knew how to use version control and was still learning the basics of OOP. Sorry for the hard to read code but I had to learn somehow. While the project works I didn't want to leave it in it's current condition. This will soon be fixed starting with tests and refactoring. I am also going to break up this code base some more making it easier to read. Please wait for a later version to use. I will have this unknotted soon.

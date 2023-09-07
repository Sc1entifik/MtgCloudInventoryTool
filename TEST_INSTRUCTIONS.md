# Testing Instructions

Pytests are included with this project module. Unlike most tests these need to be run in a particular order. 

    - Run test_entry_forms_and_databases.py first due to this test creating a new copy of scryfall_default-cards.json and optimizing it.
    
    - Run test_inventory_csv_generator.py second due to this test running way faster with scryfall_default-cards.json being optimized.

## Other points

    - Run these tests with the -s flag in order to see the dictionary references working and other useful info. 

    - There is a small issue with multiple versions of a card showing up in reference to more than one collector number. I'm mulling over whether or not this issue needs to be addressed. For now take alt-art cards, separate them and add them manually. I know that sucks however there are way fewer of these in volume compared to normal cards. I also like the simplicity and cleanliness of my codebase and don't want to end up with a Frankenstein's monster over this. I'm toying with some ideas. If anyone has any easy solutions I'm overlooking please let me know.

    - These tests are only for development purposes. Feel free to discard or ignore the test files if you are uninterested in the project code as the code pushed to the repo has already passed the tests. 

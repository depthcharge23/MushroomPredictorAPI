"""
    Mushroom_Map.py was created to store each mushroom property and its stored value and user friendly value.

    The top level of the map is the property of the mushroom. The next level is the stored value as a key, and
    the user friendly value as a value. Key "0" for each object is a list of the user friendly values to save computation
    time from having to generate lists of the user friendly values.

    Author:
        Aaron M. Mathews
    
    Date:
        5/19/2020
"""

class Mushroom_Map:
    data = {
        'class': {
            0: ['Poisonous', 'Edible'],
            1: 'Poisonous',
            2: 'Edible'
        },
        'cap-shape': {
            0: ['Bell', 'Conical', 'Convex', 'Flat', 'Knobbed', 'Sunken'],
            1: 'Bell',
            2: 'Conical',
            3: 'Convex',
            4: 'Flat',
            5: 'Knobbed',
            6: 'Sunken'
        },
        'cap-surface': {
            0: ['Fibrous', 'Grooves', 'Scaly', 'Smooth'],
            1: 'Fibrous',
            2: 'Grooves',
            3: 'Scaly',
            4: 'Smooth'
        },
        'cap-color': {
            0: ['Brown', 'Buff', 'Cinnamon', 'Gray', 'Green', 'Pink', 'Purple', 'Red', 'White', 'Yellow'],
            1: 'Brown',
            2: 'Buff',
            3: 'Cinnamon',
            4: 'Gray',
            5: 'Green',
            6: 'Pink',
            7: 'Purple',
            8: 'Red',
            9: 'White',
            10: 'Yellow'
        },
        'bruises': {
            0: ['Yes', 'No'],
            1: 'Yes',
            2: 'No'
        },
        'odor': {
            0: ['Almond', 'Anise', 'Creosote', 'Fishy', 'Foul', 'Musty', 'Pungent', 'Spicy', 'None'],
            1: 'Almond',
            2: 'Anise',
            3: 'Creosote',
            4: 'Fishy',
            5: 'Foul',
            6: 'Musty',
            7: 'Pungent',
            8: 'Spicy',
            9: 'None'
        },
        'gill-attachment': {
            0: ['Attached', 'Descending', 'Free', 'Notched'],
            1: 'Attached',
            2: 'Descending',
            3: 'Free',
            4: 'Notched'
        },
        'gill-spacing': {
            0: ['Close', 'Crowded', 'Distant'],
            1: 'Close',
            2: 'Crowded',
            3: 'Distant'
        },
        'gill-size': {
            0: ['Broad', 'Narrow'],
            1: 'Broad',
            2: 'Narrow'
        },
        'gill-color': {
            0: ['Black', 'Brown', 'Buff', 'Chocolate', 'Gray', 'Green', 'Orange', 'Pink', 'Purple', 'Red', 'White', 'Yellow'],
            1: 'Black',
            2: 'Brown',
            3: 'Buff',
            4: 'Chocolate',
            5: 'Gray',
            6: 'Green',
            7: 'Orange',
            8: 'Pink',
            9: 'Purple',
            10: 'Red',
            11: 'White',
            12: 'Yellow'
        },
        'stalk-shape': {
            0: ['Enlarging', 'Tapering'],
            1: 'Enlarging',
            2: 'Tapering'
        },
        'stalk-root': {
            0: ['Bulbous', 'Club', 'Cup', 'Equal', 'Rhizomorphs', 'Rooted', 'Missing'],
            1: 'Bulbous',
            2: 'Club',
            3: 'Cup',
            4: 'Equal',
            5: 'Rhizomorphs',
            6: 'Rooted',
            7: 'Missing'
        },
        'stalk-surface-above-ring': {
            0: ['Fibrous', 'Scaly', 'Silky', 'Smooth'],
            1: 'Fibrous',
            2: 'Scaly',
            3: 'Silky',
            4: 'Smooth'
        },
        'stalk-surface-below-ring': {
            0: ['Fibrous', 'Scaly', 'Silky', 'Smooth'],
            1: 'Fibrous',
            2: 'Scaly',
            3: 'Silky',
            4: 'Smooth'
        },
        'stalk-color-above-ring': {
            0: ['Brown', 'Buff', 'Cinnamon', 'Gray', 'Orange', 'Pink', 'Red', 'White', 'Yellow'],
            1: 'Brown',
            2: 'Buff',
            3: 'Cinnamon',
            4: 'Gray',
            5: 'Orange',
            6: 'Pink',
            7: 'Red',
            8: 'White',
            9: 'Yellow'
        },
        'stalk-color-below-ring': {
            0: ['Brown', 'Buff', 'Cinnamon', 'Gray', 'Orange', 'Pink', 'Red', 'White', 'Yellow'],
            1: 'Brown',
            2: 'Buff',
            3: 'Cinnamon',
            4: 'Gray',
            5: 'Orange',
            6: 'Pink',
            7: 'Red',
            8: 'White',
            9: 'Yellow'
        },
        'veil-type': {
            0: ['Partial', 'Universal'],
            1: 'Partial',
            2: 'Universal'
        },
        'veil-color': {
            0: ['Brown', 'Orange', 'White', 'Yellow'],
            1: 'Brown',
            2: 'Orange',
            3: 'White',
            4: 'Yellow'
        },
        'ring-number': {
            0: ['One', 'Two', 'None'],
            1: 'One',
            2: 'Two',
            3: 'None'
        },
        'ring-type': {
            0: ['Cobwebby', 'Evanescent', 'Flaring', 'Large', 'Pendant', 'Sheathing', 'Zone', 'None'],
            1: 'Cobwebby',
            2: 'Evanescent',
            3: 'Flaring',
            4: 'Large',
            5: 'Pendant',
            6: 'Sheathing',
            7: 'Zone',
            8: 'None'
        },
        'spore-print-color': {
            0: ['Black', 'Brown', 'Buff', 'Chocolate', 'Green', 'Orange', 'Purple', 'White', 'Yellow'],
            1: 'Black',
            2: 'Brown',
            3: 'Buff',
            4: 'Chocolate',
            5: 'Green',
            6: 'Orange',
            7: 'Purple',
            8: 'White',
            9: 'Yellow'
        },
        'population': {
            0: ['Abundant', 'Clustered', 'Numerous', 'Scattered', 'Several', 'Solitary'],
            1: 'Abundant',
            2: 'Clustered',
            3: 'Numerous',
            4: 'Scattered',
            5: 'Several',
            6: 'Solitary'
        },
        'habitat': {
            0: ['Grasses', 'Leaves', 'Meadows', 'Paths', 'Urban', 'Waste', 'Woods'],
            1: 'Grasses',
            2: 'Leaves',
            3: 'Meadows',
            4: 'Paths',
            5: 'Urban',
            6: 'Waste',
            7: 'Woods'
        }
    }
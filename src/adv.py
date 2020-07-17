from room import Room
from player import Player
from items import Items
# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

new_player = Player("Daniel", room["outside"])

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

def check_move(move):
    current = new_player.room
    if current.__dict__[f'{move}_to'] == None:
        print("\n You can't move that way, something blocks your path.\n")
    else:
        new_player.room = current.__dict__[f'{move}_to']

while True:
    current = new_player.room
    item = new_player.room.room_items
    movement_choice = ['n', 's', 'w', 'e']
    print(f"{new_player.name}, your current location is {current}.")
    print(f"\n Items in the area:")
    for i in item:
        print(i)
    print(f"------------------------------------------")
    choice = input(f"'What would you like to do?' | Move: [n, s, w, e] | Interact: [ pickup (item), drop (item), i (inventory)] | Quit: [q] |\n")

    if choice in movement_choice:
        check_move(choice)
        print(f"------------------------------------------")
    
    elif choice == "i" or choice == "inventory":
        print('\n Inventory:')
        for i in new_player.inventory:
            print(i)

    elif choice.split()[0] == "pickup":
        item_choice = choice.split()[1]
        if item_choice in items.keys():
            if items[item_choice] in item:
                new_player.pickup_item(items[item_choice])
                current.remove_item(items[item_choice])
                items[item_choice].on_pickup()
            else:
                print("\n Item isn't in this room. :(")
        else:
            print("\n Item does not exist! :(")
        
    elif choice.split()[0] == "drop":
        item_to_drop = choice.split()[1]
        if item_to_drop in items.keys():
            if items[item_to_drop] in new_player.inventory:
                new_player.drop_item(items[item_to_drop])
                current.add_item(items[item_to_drop])
                items[item_to_drop].on_drop()
            else:
                print(f"You don't own a {items[item_to_drop].name}")
        else:
            print("\n That doesn't exist! :(")

    elif choice == "q":
        print("Quitters never win, & winners never quit- \n Farewell for now ... \n")
        exit()
    
    else:
        print("\n You can't move that way, something blocks your path. \n")
class Room:
    no_of_rooms = 0   # class variable

    def __init__(self, room_name):
        self.name = room_name   # referring to a piece of data within the object
        self.description = None
        self.linked_rooms = {}
        self.item = None   # putting an instance of an object inside another object is called aggregation
        self.character = None # the character attribute will store a Character object

        Room.no_of_rooms = Room.no_of_rooms + 1 # To use a class variable use the name of the class, as opposed to the name of an object
        # Each time a Room object is created, the class variable' incremented in the constructor to keep track of the rooms created.

    # setters
    def set_name(self, room_name):
        self.name = room_name
    def set_description(self, room_description):
        self.description = room_description
    def set_item(self, item_name):
        self.item = item_name
    def set_character(self, new_character):
        self.character = new_character

    # getters
    def get_name(self):
        return self.name
    def get_description(self):
        return self.description
    def get_item(self):
        return self.item
    def get_character(self):
        return self.character

    def describe(self):
        print(self.description)

    def link_room(self, linked_room, direction):
        self.linked_rooms[direction] = linked_room
        # print(self.name + ' linked rooms: ' + repr(self.linked_rooms))

    def get_details(self):
        print(self.name)
        print('....................')
        print(self.description)
        for direction in self.linked_rooms:
            room = self.linked_rooms[direction]
            print('The ' + room.get_name() + ' is on the ' + direction)

    def move(self, direction):
        if direction in self.linked_rooms:
            return self.linked_rooms[direction]
        else:
            print('You cannot go that way.')
            return self    # the players is linked back to the room they were already in


    # @property
    # def get_item(self):
    #     return self._get_item  # attribute is protected., this attribute should not be changed directly
    #
    # @get_item.setter
    # def set_item(self, item_name):
    #     self._set_item = item_name
    #

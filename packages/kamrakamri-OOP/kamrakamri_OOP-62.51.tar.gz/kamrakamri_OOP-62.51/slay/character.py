class Character:

    def __init__(self, char_name, char_description):
        self.name = char_name
        self.description = char_description
        self.conversation = None

    def describe(self):
        print(self.name + ' is here! ' + self.description)
        #print(self.description)

    # Set what this character will say when talked to
    def set_conversation(self, conversation):
        self.conversation = conversation

    def talk(self):
        if self.conversation is not None:
            print(self.name + ' says, ' + self.conversation)
        else:
            print(self.name + ' does not wanna talk.')

    def fight(self, combat_item):
        print(self.name + ' does not wanna fight.')
        return True

class Enemy(Character):
    enemies_to_defeat = 0

    def __init__(self, char_name, char_description):
                        # the subclass will no longer inherit the superclass’ __init__()
        super(Enemy, self).__init__(char_name, char_description)
                        # by doing this the `Enemy` class will call the constructor of the `Character` superclass
                        # it's like, ‘To make an Enemy, first make a Character object and then customise it'
                        # the `Character` constructor sets up the attributes for the class
                        # saves from rewriting previously built methods
        self.weakness = None
        Enemy.enemies_to_defeat = Enemy.enemies_to_defeat + 1

    def set_weakness(self, item_weakness):
        self.weakness = item_weakness

    def get_weakness(self):
        return self.weakness

    def fight(self, combat_item):
        if combat_item == self.weakness:
            print('You fend ' + self.name + ' off with the ' + combat_item)
            Enemy.enemies_to_defeat = Enemy.enemies_to_defeat - 1
            return True         # if the player survives
        else:
            print(self.name + ' crushes you, puny adventurer')
            return False # if doesn't survive

    def steal(self):
        print('You stole from '  + self.name)

class Friend(Character):

    def __init__(self, char_name, char_description):
        super(Friend, self).__init__(char_name, char_description)
        self.feeling = None

    def hug(self):
        print(self.name + ' hugs you back!')
#THINGS todo:
#   random order viewing
#   looks like its all good, make a redme and publish it.

import sys
import shelve
import os

#Notecard command line "app"
class Card():
    def front(self):
        self.fr = raw_input("Front of the note card (term)? : ")
        return self.fr
    def back(self):
        self.bk = raw_input("Back of the note card (definition)? : ")
        return self.bk

class set():
    i = 0
    is_on_def = False
    card_order = []
    dict_of_cards = {}

    def makeCards(self):
        a_card = Card()
        a_card.front()
        a_card.back()
        correct = raw_input("""is \"{}\"
and \"{}\"
correct? (Y or N): """.format(a_card.fr, a_card.bk))

        if correct.lower() == "y":
            try:
                if self.dict_of_cards[a_card.fr]: #if you are remaking a card
                    self.dict_of_cards[a_card.fr] = a_card.bk
            except KeyError:
                self.card_order.append(a_card.fr)
                self.dict_of_cards[a_card.fr] = a_card.bk
        else:
            print "OK, it has been discarded"
        def more_cards():
            cardsq = raw_input("do you want to make another card? (Y/N)").lower()
            if cardsq == "y":
                s.makeCards()
            elif cardsq == "n":
                return
            else:
                print "Y or N only"
                return more_cards()
        return more_cards()

    def study(self):
        def viewing_controls():
            user_keypress = raw_input("N for next, P for previous, F to flip, Q to quit, C to edit: ")
            if user_keypress.lower() == "n":
                os.system('cls' if os.name == 'nt' else 'clear')
                return nextthing
            elif user_keypress.lower() == "p":
                os.system('cls' if os.name == 'nt' else 'clear')
                return prev
            elif user_keypress.lower() == "f":
                os.system('cls' if os.name == 'nt' else 'clear')
                return flip
            elif user_keypress.lower() == "q":
                os.system('cls' if os.name == 'nt' else 'clear')
                print "Exiting"
                sys.exit(0)
            elif user_keypress.lower() == "c":
                os.system('cls' if os.name == 'nt' else 'clear')
                s.makeCards()
                backup()
                s.study()
            else:
                print "That was not a valid key"
                return viewing_controls()
        def nextthing():
            if (self.i <  (len(self.card_order)-1)):
                self.i += 1
                st = "#"
                st = format(st, '#<{}'.format (len(self.card_order[self.i]) + 20))
                print """
        {}
                    {}
        {}""".format(st, self.card_order[self.i], st)
                self.is_on_def = False
            else:
                self.i = 0
                st = "#"
                st = format(st, '#<{}'.format (len(self.card_order[self.i]) + 20))
                print """
        {}
                    {}
        {}""".format(st, self.card_order[self.i], st)
                self.is_on_def = False
        def prev():
            if self.i == 0:
                self.i = (len(self.card_order) - 1)
                st = "#"
                st = format(st, '#<{}'.format (len(self.card_order[self.i]) + 20))
                print """
        {}
                    {}
        {}""".format(st, self.card_order[self.i], st)
                self.is_on_def = False
            else:
                self.i -= 1
                st = "#"
                st = format(st, '#<{}'.format (len(self.card_order[self.i]) + 20))
                print """
        {}
                    {}
        {}""".format(st, self.card_order[self.i], st)
                self.is_on_def = False
        def flip():
            if not self.is_on_def:
                st = "#"
                st = format(st, '#<{}'.format (len(self.dict_of_cards[self.card_order[self.i]]) + 20))
                print """
        {}
                    {}
        {}""".format(st, self.dict_of_cards[self.card_order[self.i]], st)
                self.is_on_def = True
            else:
                st = "#"
                st = format(st, '#<{}'.format (len(self.card_order[self.i]) + 20))
                print """
        {}
                    {}
        {}""".format(st, self.card_order[self.i], st)
                self.is_on_def = False

        try:
            st = "#"
            st = format(st, '#<{}'.format (len(self.card_order[self.i]) + 20))
            print """
        {}
                    {}
        {}""".format(st, self.card_order[self.i], st)
            is_on_def = False
        except IndexError:
            print "no cards in set"
            sys.exit(1)
        while True:
            viewing_controls()()

def backup():
    save = raw_input("would you like to save this set? (Y or N)")
    if save.lower() == "y":
        database = shelve.open("notecards")
        name = raw_input("what would you like to call this set?")
        database[name] = [s.card_order,s.dict_of_cards] #the improtant data for loading a set
        database.close()
        return
    elif save.lower() == "n":
        return
    else:
        print "Y or N only"
        return backup()

def open_backup():   #Return is True if set is loaded and False otherwise
    database = shelve.open("notecards")
    avalible_sets = [] #sets made and saved
    for key in database:
        avalible_sets.append(key)
    if avalible_sets:
        print "avalible sets:"
        print avalible_sets
        set = raw_input("which set would you like to open?")
        for avalible_set in avalible_sets:
            if set == avalible_set:
                s.card_order = (database[avalible_set])[0]
                s.dict_of_cards = (database[avalible_set])[1] #for clarification look at backup()
                print "set found and loaded"
                return True
        if not s.card_order:
            print "set not found"
            return False
    else:
        print "No sets saved"
        return False

    database.close()

s = set()
def main():
    set_loaded = open_backup() #boolean
    if not set_loaded:
        s.makeCards()
        backup()
        s.study()
    else:
        s.study()
main()

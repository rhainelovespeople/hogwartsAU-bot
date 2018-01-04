import random

########################################
## GLOBALS
locations = []
coffee = {
    'endings': [], 
    'modifiers': [],
    'types': [],
    'menu': []
}
########################################

def randChoice(choices, weights=None):
    if weights==None:
        return random.choice(choices)
    total = sum(weights)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(choices, weights):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"

class Character:
    def __init__(self, roles, name, whichExtras=[]):
        self.name = name
        self.roles = roles
        self.extras = {}
        for key in whichExtras:
            self.extras[key] = []
        # self.house = house
    def addExtra(self, keyName, item):
        self.extras[keyName].append(item)
    def getExtra(self, keyName):
        if keyName in self.extras:
            return self.extras[keyName]
        else:
            raise Exception("No such extra for %s" % self.name)
        

# string -> Character
def searchByName(name):
    for c in characters:
        if c.name==name:
            return c
# [String] -> [Character]
def selectRole(requiredRoles):
    return list(filter(lambda c: all([role in c.roles for role in requiredRoles]),
                  characters))

def deductOrGive(points):
    if points<0:
        return "deducted " + str(abs(points)) + " points"
    else:
        return "gave " + str(abs(points)) + " points"

# takes (string, [list of things to fill string with])
# chooses one option for each thing in list, fills string
# e.g. ("{} will die tomorrow", ['name']) may result in "Marc will die tomorrow"
# valid options are 'name', 'location'
def fillOptions(phrase):
    fillWith = []
    for a in phrase[1]:
        if a == 'name':
            fillWith.append(randChoice([c.name for c in characters]))
        elif a == 'location':
            fillWith.append(randChoice(locations))
        elif a[0:5] == 'name:':
            role = a[5:]
            fillWith.append(randChoice( [c.name for c in selectRole([role])] ))
        
    return phrase[0].format(*fillWith)


def loadStuff():
    # locations
    with open('locations.txt') as f:
        for line in f:
            locations.append(line[:-1]) # removes last character (newline)
    # character extras
    for name in ['Marc', 'Ru', 'Sasha']:
        student = searchByName(name)
        for extra in student.extras:    #['beliefs','powers','adjectives','nouns']:
            with open('%s%s.txt' % (extra, name)) as f:
                for line in f:
                    student.addExtra(extra, line[:-1])
    # coffee things
    for part in coffee:
        with open('coffee/coffee%s.txt' % (part)) as f:
            for line in f:
                coffee[part].append(line[:-1])
            
                    
divinations = [ ("{} will die a horrible death", ['name:Student']),
                ("{} and {} will marry and then die", ['name:Student', 'name:Student']),
                ("Nobody will pass Professor {}'s quiz this year", ['name:Professor']),
                ("{} will become the new Dark Lord", ['name']),
                ("{} will get a Troll on the Transfiguration O.W.L.", ['name:Student']),
                ("Careful with the teacups today {} dear", ['name:Student']),
                ("The grim! THE GRIM! Oh wait no it's just {}", ['name'])
              ]
    
characters = [Character(['Main', 'Student'], 'Ru', ['beliefs','powers','adjectives','nouns']),
              Character(['Main', 'Student'], 'Marc', ['beliefs','powers','adjectives','nouns']),
              Character(['Main', 'Student'], 'Sasha', ['beliefs','powers']),
              Character(['Student'], 'Luke')] + \
    [Character(['Professor'], prof) for prof in [
        'Dumbledore','McGonagall','Flitwick','Quirrel','Snape','Sprout',
        'Lupin', 'Moody', 'Hagrid', 'Hooch']]

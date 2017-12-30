import random

def randChoice(choices, weights=None):
    if weights==None:
        return random.choice(choices)
    total = sum(w for w in weights)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(choices, weights):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"

class Character:
    def __init__(self, roles, name):
        self.name = name
        self.roles = roles
        # self.house = house
    def setBeliefs(self, beliefs):
        self.beliefs = beliefs
    def setPowers(self, powers):
        self.powers = powers

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



locations = []
#all files should end in a newline
def loadStuff():
    with open('locations.txt') as f:
        for line in f:
            locations.append(line[:-1]) # removes last character (newline)
    for name in ['Marc', 'Ru']:
        with open('beliefs%s.txt' % name) as f:
            beliefs=[]
            for line in f:
                beliefs.append(line[:-1])
            searchByName(name).setBeliefs(beliefs)
        with open('powers%s.txt' % name) as f:
            powers=[]
            for line in f:
                powers.append(line[:-1])
            searchByName(name).setPowers(powers)
            
divinations = [ ("{} will die a horrible death", ['name:Student']),
                ("{} and {} will marry and then die", ['name:Student', 'name:Student']),
                ("Nobody will pass Professor {}'s quiz this year", ['name:Professor']),
                ("{} will become the new Dark Lord", ['name']),
                ("{} will get a Troll on the Transfiguration O.W.L.", ['name:Student']),
                ("Careful with the teacups today {} dear", ['name:Student']),
                ("The grim! THE GRIM! Oh wait no it's just {}", ['name'])
              ]
    
characters = [Character(['Main', 'Student'], 'Ru'),
              Character(['Main', 'Student'], 'Marc'),
              Character(['Student'], 'Luke')] + \
    [Character(['Professor'], prof) for prof in [
        'Dumbledore','McGonagall','Flitwick','Quirrel','Snape','Sprout',
        'Lupin', 'Moody', 'Hagrid', 'Hooch']]

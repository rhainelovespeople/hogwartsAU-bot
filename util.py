import random
import ruamel.yaml
from ruamel.yaml.util import load_yaml_guess_indent

########################################
## GLOBALS
locations = []
coffee = {
    'endings': [],
    'modifiers': [],
    'types': [],
}
coffeeMenu = []
events = []
phrases = []
#the shape controls how skewed it is: larger -> more centered, smaller -> more skewed, mode closer to 0
coffeeShape = 2.0
coffeeScale = 2.0
coffeeShopName = "Quirky Defense Against the Dark sleep-Deprived You"
coffeeShopAbbrev = "Quirky DADDY"
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

class Coffee:
    def __init__(self, name, sales=0, creatorName=None, price=None):
        self.name = name
        self.price = price
        self.sales = sales
        self.creatorName = creatorName # not necessarily a character
    def __str__(self):
        return '%s;%d;%s;%s;' %(self.name,self.sales,self.creatorName,self.price)
    def updateSales(self,sales):
        for i in range(len(coffeeMenu)):
            if self.name==coffeeMenu[i].name:
                coffeeMenu[i].sales+=sales
                with open('coffee/coffeemenu.txt', 'w') as f:
                    for c in coffeeMenu:
                        f.write(str(c)+'\n')
                return
        with open('coffee/coffeemenu.txt','a') as f:
            coffeeMenu.append(self)
            f.write(str(self)+'\n')

class Event:
    def __init__(self, name, triggerSales, triggerState='no'):
        self.name = name
        self.triggerSales = triggerSales
        self.triggerState = triggerState
        self.effects = None
    def __str__(self):
        return '%s;%d;%s;' %(self.name,self.triggerSales,self.triggerState)

    def setEffects(self, effects):
        self.effects = effects

def checkEvents():
    for e in events:
        if e.triggerState=='no' \
        and e.triggerSales <= sum([c.sales for c in coffeeMenu]):
            if e.effects != None:
                print(e.effects()) # tweet this probably
                e.triggerState='yes'
                with open('events.txt', 'w') as f:
                    for e in events:
                        f.write(str(e)+'\n')

# string -> Character
def searchByName(name):
    for c in characters:
        if c.name==name:
            return c

def searchEventsByName(name):
    for e in events:
        if e.name==name:
            return e

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

def reset():
    open('coffee/coffeemenu.txt', 'w').close()
    with open('coffee/gammadistribution.txt', 'w') as f:
        f.write('%f\n%f' % (coffeeShape, coffeeScale))
    with open('events.txt', 'r') as f:
        newFile = ""
        for line in f:
            array = line.split(';')
            array[2] = 'no'
            newFile += ';'.join(array)
    with open('events.txt', 'w') as f:
        f.write(newFile)

def loadStuff():
    # locations
    with open('locations.txt') as f:
        for line in f:
            locations.append(line[:-1]) # removes last character (newline)
    # character extras
    for name in ['Marc', 'Ru', 'Sasha', 'Leo']:
        student = searchByName(name)
        for extra in student.extras:    #['beliefs','powers','adjectives','nouns']:
            with open('characters/%s/%s%s.txt' % (name.lower(), extra, name)) as f:
                for line in f:
                    student.addExtra(extra, line[:-1])
    # coffee things
    for part in ["modifiers", "endings", "types"]:
        with open('coffee/coffee%s.txt' % (part)) as f:
            for line in f:
                coffee[part].append(line[:-1])
    with open('coffee/coffeemenu.txt') as f:
        for line in f:
            array = line.split(';')
            if array[2] == 'None':
                creatorName = None
            else:
                creatorName = array[2]
            if array[3] == 'None':
                price = None
            else:
                price = array[3]

            c = Coffee(array[0],int(array[1]),creatorName,price)
            coffeeMenu.append(c)
    with open('coffee/gammadistribution.txt') as f:
        coffeeShape= float(f.readline())
        coffeeScale = float(f.readline())
    # event things
    with open('events.txt') as f:
        for line in f:
            array = line.split(';')
            events.append(Event(array[0], int(array[1]), array[2]))

divinations = [ ("{} will die a horrible death", ['name:Student']),
                ("{} and {} will marry and then die", ['name:Student', 'name:Student']),
                ("Nobody will pass Professor {}'s quiz this year", ['name:Professor']),
                ("{} will become the new Dark Lord", ['name:Student']),
                ("{} will get a Troll on the Transfiguration O.W.L.", ['name:Student']),
                ("Careful with the teacups today {} dear", ['name:Student']),
                ("The grim! THE GRIM! Oh wait no it's just {}", ['name:Student'])
              ]

characters = [Character(['Main', 'Student'], 'Ru', ['beliefs','powers','adjectives','nouns']),
              Character(['Main', 'Student'], 'Marc', ['beliefs','powers','adjectives','nouns']),
              Character(['Main', 'Student'], 'Sasha', ['beliefs','powers']),
              Character(['Main', 'Student'], 'Leo', ['beliefs','adjectives','nouns']),
              Character(['Student'], 'Luke')]
characters += [Character(['Professor'], prof) for prof in [
        'Dumbledore','McGonagall','Flitwick','Quirrel','Snape','Sprout',
        'Lupin', 'Moody', 'Hagrid', 'Hooch']]

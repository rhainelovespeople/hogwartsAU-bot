import tweepy
from util import *
import random

from secrets import *

"""auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)"""

#for prof
#graded [student]
#it said 'student thingy'
#+- n points
def profGraded():
    professor = randChoice(selectRole(['Professor']))
    student = randChoice(selectRole(['Main', 'Student']))
    belief = randChoice(student.getExtra('beliefs'))
    points = randChoice(map(deductOrGive,
                            [-100,-50,-20,-10,-5,-1,-0.1,-0.001,0.29, 1, 5,10,30,1000]),
                            [   2,  3, 10, 20,30,35,  10,     5,  10,35,30,20, 5,   1])
    return "%s was grading %s's homework. It said \"%s\", so professor %s." % (
        professor.name,student.name,belief,points)

def wallWriting():
    student = randChoice(selectRole(['Main', 'Student']))
    belief = randChoice(student.getExtra('beliefs'))
    location = randChoice(locations)
    return '%s was caught by %s halfway through writing "%s" in big red letters.'\
        % (student.name, location, belief)

def divination():
    return 'During Divination, Trelawney said, "%s".' % (
        fillOptions(randChoice(divinations)))

def armyWin():
    student = randChoice(selectRole(['Main','Student']))
    power = randChoice(student.getExtra('powers'))
    return '%s brought victory to their Quirrel army by %s.'\
        % (student.name, power)

def armyName():
    student = randChoice(selectRole(['Main','Student']))
    noun = randChoice(student.getExtra('nouns'))
    adjective = randChoice(student.getExtra('adjectives'))
    return '%s became a General of a Quirrel army. They\'re thinking of naming it "%s %s".'\
        % (student.name, adjective, noun)

def newCoffeeSale():
    flavourArray = []
    for _ in range(randChoice([1,2], [2,1])):
        flavourArray.append(randChoice(coffee['modifiers']))
    for _ in range(randChoice([1,2], [3,1])):
        flavourArray.append(randChoice(coffee['endings']))
    flavourArray.append(randChoice(coffee['types']))

    #shape, scale
    #the shape controls how skewed it is: larger -> more centered, smaller -> more skewed, mode closer to 0
    sales = int(round(random.gammavariate(coffeeShape,coffeeScale)))

    flavour = ' '.join(flavourArray)
    salesPlural = 'sale' if sales==1 else 'sales'

    if searchEventsByName('hufflepuffGirl').triggerState == 'yes':
        madeBy = coffeeShopAbbrev
    else:
        madeBy = 'Ru'

    c = Coffee(flavour,sales,madeBy)
    c.updateSales()

    return '%s introduced a new coffee flavour: "%s". It made %d %s!' % (
        madeBy,flavour,sales,salesPlural)

def characterThemedCoffee():
    character = randChoice(selectRole(['Main']))
    adjective = randChoice(character.getExtra('adjectives'))
    flavourArray = [adjective]
    for _ in range(randChoice([0,1], [1,1])):
        flavourArray.append(randChoice(coffee['modifiers']))
    for _ in range(randChoice([1,2], [3,1])):
        flavourArray.append(randChoice(coffee['endings']))
    flavourArray.append(randChoice(coffee['types']))

    flavour = ' '.join(flavourArray)
    c = Coffee(flavour, 1, character.name)
    c.updateSales()

    return '%s made their own flavour of coffee at %s: "%s"!' % (
        character.name, coffeeShopAbbrev, flavour)

def hufflepuffGirlEvent():
    coffeeScale = 4.0
    with open('coffee/gammadistribution.txt','w') as f:
        f.write('%f\n%f' % (coffeeShape, coffeeScale))
    return 'Gillian has joined Ru to create the first Hogwarts coffee chain\
: "%s"!' % coffeeShopName

if __name__ == "__main__":
    reset()
    loadStuff()
    searchEventsByName("hufflepuffGirl").setEffects(hufflepuffGirlEvent)
    checkEvents()

    i = 0
    while i<5:
        try:
            f = newCoffeeSale
            #f = randChoice([newCoffeeSale, characterThemedCoffee, armyName, divination, profGraded, wallWriting, armyWin])
            print(f())
            i+=1
        except Exception as e:
            pass
        checkEvents()
    checkEvents()

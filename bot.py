import tweepy
from util import *
import random

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
    sales = int(round(random.gammavariate(2,2)))
    
    flavour = ' '.join(flavourArray)
    salesPlural = 'sale' if sales==1 else 'sales'

    return 'Ru introduced a new coffee flavour: "%s". It made %d %s!' % (flavour,sales,salesPlural)
    
loadStuff()
i = 0
while i<5:
    try:
        f = randChoice([newCoffeeSale]) #[armyName, divination, profGraded, wallWriting, armyWin])
        print(f())
        i+=1
    except Exception as e:
        i-=1

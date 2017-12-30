#for prof
#graded [student]
#it said 'student thingy'
#+- n points
def profGraded():
    professor = randChoice(selectRole(['Professor']))
    student = randChoice(selectRole(['Main', 'Student']))
    belief = randChoice(student.beliefs)
    points = randChoice(map(deductOrGive,
                            [-100,-50,-20,-10,-5,-1,-0.1,-0.001,0.29, 1, 5,10,30,1000]),
                            [   2,  3, 10, 20,30,35,  10,     5,  10,35,30,20, 5,   1])
    return "%s was grading %s's homework. It said \"%s\", so professor %s." % (
        professor.name,student.name,belief,points) 

def wallWriting():
    student = randChoice(selectRole(['Main', 'Student']))
    belief = randChoice(student.beliefs)
    location = randChoice(locations)
    return '%s was caught by %s halfway through writing "%s" in big red letters.'\
        % (student.name, location, belief)
        
def divination():
    return 'During Divination, Trelawney said, "%s".' % (
        fillOptions(randChoice(divinations)))

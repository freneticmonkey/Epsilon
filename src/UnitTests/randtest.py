
import random

_rand = random
_rand.seed(12341234)

value = 0
while value < 10:
    randValue = _rand.random()
    print 'Random: ' + str(randValue)
    value += 1
    
    if value == 5:
        print 'test random seeded values'
        _newRand = random
        _newRand.seed(randValue)
        nLC = 0
        while nLC < 5:
            nRandValue = _newRand.random()
            print '    New Random: ' + str(nRandValue)
            nLC += 1
        
_rand = random
_rand.seed(12341234)
print 'And again...\n'

value = 0
while value < 10:
    randValue = _rand.random()
    print 'Random: ' + str(randValue)
    value += 1
        
    if value == 5:
        print 'test random seeded values'
        _newRand = random
        _newRand.seed(randValue)
        nLC = 0
        while nLC < 5:
            nRandValue = _newRand.random()
            print '    New Random: ' + str(nRandValue)
            nLC += 1
    
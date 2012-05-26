
class Random:
    def __init__(self, range, seed):
        self._range = range
        self._seed = seed
        self._result = -1
        self._ulGen1 = 65536
        self._ulGen2 = self._ulGen1 * 2 
        self._ulMax = range
                
    def _generateNumber(self):
        self._seed = self._ulGen1 * self._seed
        self._seed = self._seed + self._ulGen2
        
        self._seed = (self._seed / self._ulMax ) % self._ulMax
        self._result = self._seed 
                       
        return self._result
   
#_rand = Random(200, 35354)
#value = 0
#while value < 100:
#    print 'Random Returned: ' + str(_rand._generateNumber())
#    value+=1